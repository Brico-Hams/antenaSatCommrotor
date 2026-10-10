package org.bricohams.portablesatstation

import android.annotation.SuppressLint
import android.bluetooth.*
import android.content.Context
import android.os.Build
import android.os.Handler
import android.os.Looper
import org.json.JSONObject
import java.util.ArrayDeque

/** One GATT operation and one application request in flight; all state is confined to the main looper. */
@SuppressLint("MissingPermission")
class BleTransport(private val context: Context, private val listener: Listener) {
    interface Listener {
        fun onStatus(status: RotorStatus)
        fun onResponse(operation: String, body: JSONObject)
        fun onFailure(code: String)
        fun onDisconnected()
    }
    private val main = Handler(Looper.getMainLooper())
    private var gatt: BluetoothGatt? = null
    private var rx: BluetoothGattCharacteristic? = null
    private var tx: BluetoothGattCharacteristic? = null
    private val session = ControlSession()
    private var mtu = 23
    private var mtuRetry = false
    private var stage = Stage.DISCONNECTED
    private val fragments = ArrayDeque<ByteArray>()
    private val assembler = FrameAssembler()
    private var emergencyStop = false
    private var writing = false
    private var operationRetry = 0
    private var completedResponse: ByteArray? = null
    val ready: Boolean get() = session.authenticated
    val busy: Boolean get() = session.pending != null || writing
    private enum class Stage { DISCONNECTED, CONNECTING, SERVICES, MTU, SUBSCRIBING, HANDSHAKE, READY }
    private val timeout = Runnable { fail("ble_request_timeout") }

    fun connect(device: BluetoothDevice, token: String) {
        check(Looper.myLooper() == Looper.getMainLooper())
        disconnect()
        if (device.bondState != BluetoothDevice.BOND_BONDED || token.isEmpty()) {
            listener.onFailure("bond_and_token_required"); return
        }
        session.start(token); stage = Stage.CONNECTING
        gatt = device.connectGatt(context, false, callback, BluetoothDevice.TRANSPORT_LE)
        if (gatt == null) fail("connect_failed") else armTimeout()
    }
    fun disconnect() {
        main.removeCallbacks(timeout)
        val previous = gatt
        gatt = null; rx = null; tx = null; stage = Stage.DISCONNECTED
        session.reset(); emergencyStop = false
        fragments.clear(); assembler.reset(); completedResponse = null; writing = false; mtu = 23; mtuRetry = false
        try { previous?.disconnect() } catch (_: SecurityException) { listener.onFailure("permission_denied") }
        try { previous?.close() } catch (_: SecurityException) { listener.onFailure("permission_denied") }
        listener.onDisconnected()
    }
    fun command(operation: String, body: JSONObject, priority: Boolean = false) {
        if (!ready) { listener.onFailure("not_authenticated"); return }
        if (busy) {
            if (priority && operation == "stop") emergencyStop = true
            else listener.onFailure("request_busy")
            return
        }
        submit(operation, body)
    }
    private fun submit(operation: String, body: JSONObject) {
        try {
            val request = session.create(operation, body)
            fragments.addAll(Protocol.frames(request.bytes, mtu))
            assembler.reset(); operationRetry = 0
            armTimeout(); writeNext()
        } catch (error: ProtocolFailure) { fail(error.code) }
        catch (_: SecurityException) { fail("permission_denied") }
    }
    private fun armTimeout() { main.removeCallbacks(timeout); main.postDelayed(timeout, 15000) }
    private fun fail(code: String) { disconnect(); listener.onFailure(code) }
    private fun dispatch(source: BluetoothGatt, action: () -> Unit) {
        main.post {
            if (source !== gatt) return@post
            try { action() } catch (_: SecurityException) { fail("permission_denied") }
            catch (error: ProtocolFailure) { fail(error.code) }
        }
    }
    private fun negotiate() {
        stage = Stage.MTU; armTimeout()
        val accepted = gatt?.requestMtu(if (mtuRetry) 23 else 185) == true
        if (!accepted) {
            if (!mtuRetry) {
                mtuRetry = true
                main.postDelayed({
                    try { if (stage == Stage.MTU) negotiate() }
                    catch (_: SecurityException) { fail("permission_denied") }
                }, 250)
            }
            else fail("mtu_negotiation_failed")
        }
    }
    private fun subscribe() {
        stage = Stage.SUBSCRIBING; armTimeout()
        val connection = gatt ?: return
        val characteristic = tx ?: return fail("gatt_contract_missing")
        if (!connection.setCharacteristicNotification(characteristic, true)) return fail("notification_failed")
        val descriptor = characteristic.getDescriptor(Protocol.CCCD) ?: return fail("cccd_missing")
        val accepted = if (Build.VERSION.SDK_INT >= 33)
            connection.writeDescriptor(descriptor, BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE) == BluetoothStatusCodes.SUCCESS
        else {
            @Suppress("DEPRECATION")
            descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            @Suppress("DEPRECATION")
            connection.writeDescriptor(descriptor)
        }
        if (!accepted) fail("notification_subscribe_failed")
    }
    private fun writeNext() {
        if (writing || fragments.isEmpty()) return
        val connection = gatt ?: return
        val characteristic = rx ?: return fail("gatt_contract_missing")
        val bytes = fragments.first
        val accepted = if (Build.VERSION.SDK_INT >= 33)
            connection.writeCharacteristic(characteristic, bytes, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT) == BluetoothStatusCodes.SUCCESS
        else {
            @Suppress("DEPRECATION")
            characteristic.value = bytes
            characteristic.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
            @Suppress("DEPRECATION")
            connection.writeCharacteristic(characteristic)
        }
        if (accepted) writing = true
        else if (operationRetry++ < 2) main.postDelayed({
            try { if (gatt === connection) writeNext() } catch (_: SecurityException) { fail("permission_denied") }
        }, 100)
        else fail("gatt_write_start_failed")
    }
    private fun notification(value: ByteArray) {
        if (session.pending == null || completedResponse != null) throw ProtocolFailure("unsolicited_response")
        val bytes = assembler.feed(value) ?: return
        if (fragments.size > 1) throw ProtocolFailure("response_before_write_complete")
        completedResponse = bytes
        if (!writing && fragments.isEmpty()) finishResponse()
    }
    private fun finishResponse() {
        val bytes = completedResponse ?: return
        completedResponse = null
        val request = session.pending ?: throw ProtocolFailure("unsolicited_response")
        val response = session.accept(bytes)
        main.removeCallbacks(timeout)
        if (request.operation == "status") {
            val status = RotorStatus.parse(response.data)
            if (stage == Stage.HANDSHAKE) stage = Stage.READY
            listener.onStatus(status)
        } else listener.onResponse(request.operation, response.data)
        if (emergencyStop) { emergencyStop = false; submit("stop", JSONObject()) }
    }
    private val callback = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(source: BluetoothGatt, status: Int, newState: Int) = dispatch(source) {
            if (status != BluetoothGatt.GATT_SUCCESS || newState == BluetoothProfile.STATE_DISCONNECTED)
                fail("connection_lost_$status")
            else if (newState == BluetoothProfile.STATE_CONNECTED && stage == Stage.CONNECTING) {
                if (source.device.bondState != BluetoothDevice.BOND_BONDED) return@dispatch fail("bond_lost")
                stage = Stage.SERVICES; armTimeout()
                if (!source.discoverServices()) fail("service_discovery_failed")
            }
        }
        override fun onServicesDiscovered(source: BluetoothGatt, status: Int) = dispatch(source) {
            if (stage != Stage.SERVICES) return@dispatch
            if (status != BluetoothGatt.GATT_SUCCESS) return@dispatch fail("service_discovery_failed")
            val service = source.getService(Protocol.SERVICE) ?: return@dispatch fail("gatt_contract_missing")
            rx = service.getCharacteristic(Protocol.RX); tx = service.getCharacteristic(Protocol.TX)
            if (rx == null || tx == null || rx!!.properties and BluetoothGattCharacteristic.PROPERTY_WRITE == 0 ||
                tx!!.properties and BluetoothGattCharacteristic.PROPERTY_NOTIFY == 0)
                return@dispatch fail("gatt_contract_missing")
            negotiate()
        }
        override fun onMtuChanged(source: BluetoothGatt, value: Int, status: Int) = dispatch(source) {
            if (stage != Stage.MTU) return@dispatch
            if (status != BluetoothGatt.GATT_SUCCESS || value < 23) {
                if (!mtuRetry) { mtuRetry = true; negotiate() } else fail("mtu_negotiation_failed")
            } else { mtu = value; subscribe() }
        }
        override fun onDescriptorWrite(source: BluetoothGatt, descriptor: BluetoothGattDescriptor, status: Int) = dispatch(source) {
            if (stage != Stage.SUBSCRIBING || descriptor.uuid != Protocol.CCCD) return@dispatch
            if (status != BluetoothGatt.GATT_SUCCESS) return@dispatch fail("encrypted_subscription_failed")
            stage = Stage.HANDSHAKE; submit("status", JSONObject())
        }
        override fun onCharacteristicWrite(source: BluetoothGatt, characteristic: BluetoothGattCharacteristic, status: Int) = dispatch(source) {
            if (characteristic.uuid != Protocol.RX || !writing) return@dispatch
            writing = false
            if (status != BluetoothGatt.GATT_SUCCESS) return@dispatch fail("encrypted_write_failed_$status")
            fragments.removeFirst(); operationRetry = 0
            if (completedResponse != null && fragments.isEmpty()) finishResponse() else writeNext()
        }
        @Deprecated("Used on Android 8–12")
        override fun onCharacteristicChanged(source: BluetoothGatt, characteristic: BluetoothGattCharacteristic) {
            if (Build.VERSION.SDK_INT >= 33 || characteristic.uuid != Protocol.TX) return
            @Suppress("DEPRECATION")
            val value = characteristic.value?.clone() ?: return
            dispatch(source) { notification(value) }
        }
        override fun onCharacteristicChanged(source: BluetoothGatt, characteristic: BluetoothGattCharacteristic, value: ByteArray) {
            if (characteristic.uuid != Protocol.TX) return
            val copy = value.clone()
            dispatch(source) { notification(copy) }
        }
    }
}
