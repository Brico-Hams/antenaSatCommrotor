package org.bricohams.portablesatstation

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import android.bluetooth.BluetoothProfile
import android.content.Context
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import org.json.JSONObject
import org.bricohams.portablesatstation.orbit.RotorHostApi
import java.util.ArrayDeque
import java.util.UUID
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

@SuppressLint("MissingPermission")
internal class RadioHostBleTransport(
    private val context: Context,
    private val listener: Listener
) {
    interface Listener {
        fun onState(code: String)
        fun onStatus(status: RadioHostStatus)
        fun onAudioReady(rxChannel: String, txChannel: String, mtu: Int)
        fun onAudioBlock(block: PcmBlock, channel: String)
        fun onHostEvent(path: String, data: JSONObject)
        fun onFailure(code: String)
        fun onDisconnected()
    }

    private data class Request(
        val path: String,
        val op: String,
        val data: JSONObject,
        val callback: (JSONObject?, String?) -> Unit
    )

    private val main = Handler(Looper.getMainLooper())
    private val controlAssembler = RadioHostControlAssembler()
    private val requestQueue = ArrayDeque<Request>()
    private val audioLock = Object()
    private var gatt: BluetoothGatt? = null
    private var controlRx: BluetoothGattCharacteristic? = null
    private var controlTx: BluetoothGattCharacteristic? = null
    private var audioRx: BluetoothGattCharacteristic? = null
    private var audioTx: BluetoothGattCharacteristic? = null
    private var pendingRequest: Request? = null
    private var pendingId: String? = null
    private var controlSequence = 0
    private var requestId = 1L
    private var writeFragments = ArrayDeque<ByteArray>()
    private var controlWriting = false
    private var completeControlEnvelope: ByteArray? = null
    private var stage = Stage.DISCONNECTED
    private var mtu = 0
    private var mtuRetry = false
    private var authenticated = false
    private var audioActive = false
    private var audioStopping = false
    private var rxStreamId = 0L
    private var txStreamId = 0L
    private var rxSequence = 0L
    private var rxSample = 0L
    private var txSequence = 0L
    private var txSample = 0L
    private var txCredits = 0
    private var rxChannel = ""
    private var txChannel = ""
    private var audioWriteActive = false
    private var connectionGeneration = 0L
    private val timeout = Runnable { fail("radio_host_timeout") }

    private enum class Stage {
        DISCONNECTED, CONNECTING, SERVICES, CONTROL_SUBSCRIBE, AUTHENTICATING,
        STATUS, AUDIO_SUBSCRIBE, MTU, AUDIO_START, READY
    }

    val connectedAndAuthenticated: Boolean get() = authenticated && gatt != null
    val readyForAudio: Boolean get() = stage == Stage.READY && audioActive
    val negotiatedMtu: Int get() = mtu

    fun connect(device: BluetoothDevice, token: String) {
        check(Looper.myLooper() == Looper.getMainLooper())
        disconnect(false)
        if (device.bondState != BluetoothDevice.BOND_BONDED) {
            listener.onFailure("radio_host_bond_required")
            return
        }
        if (!token.matches(Regex("[0-9a-fA-F]{64}"))) {
            listener.onFailure("radio_host_token_invalid")
            return
        }
        connectionGeneration++
        authenticated = false
        stage = Stage.CONNECTING
        listener.onState("radio_host_connecting")
        armTimeout()
        gatt = if (Build.VERSION.SDK_INT >= 23)
            device.connectGatt(context, false, callback, BluetoothDevice.TRANSPORT_LE)
        else device.connectGatt(context, false, callback)
        if (gatt == null) fail("radio_host_connect_failed")
        else authToken = token
    }

    private var authToken = ""

    fun requestStatus(onUpdated: ((RadioHostStatus?, String?) -> Unit)? = null) {
        if (!connectedAndAuthenticated || stage == Stage.DISCONNECTED) {
            listener.onFailure("radio_host_not_authenticated")
            return
        }
        enqueue(Request("/status", "get", JSONObject()) { _, error ->
            if (error != null) listener.onFailure(error)
            onUpdated?.invoke(lastStatus, error)
        })
    }

    fun requestRotorHost(
        path: String,
        operation: String,
        data: JSONObject,
        callback: (JSONObject?, String?) -> Unit
    ) {
        checkMain()
        val validationError = RotorHostApi.requestError(path, operation, data)
        if (validationError != null) {
            callback(null, validationError)
            return
        }
        enqueue(Request(path, operation, data) { response, error ->
            callback(response, error)
        })
    }

    fun startAudio(selectedRxChannel: String, selectedTxChannel: String) {
        checkMain()
        val characteristicReady = audioRx != null && audioTx != null && mtu >= 247
        if (!authenticated || stage != Stage.READY || audioActive || !characteristicReady) {
            listener.onFailure("radio_audio_not_ready")
            return
        }
        if (!RadioHostWire.validAudioChannels(selectedRxChannel, selectedTxChannel, availableChannels)) {
            listener.onFailure("radio_audio_channel_invalid")
            return
        }
        rxChannel = selectedRxChannel
        txChannel = selectedTxChannel
        stage = Stage.AUDIO_START
        val body = JSONObject().put("rate", RadioHostWire.AUDIO_RATE).put("mtu", mtu)
            .put("rxChannel", rxChannel).put("txChannel", txChannel)
        enqueue(Request("/audio/start", "set", body) { data, error ->
            if (error != null) {
                stage = Stage.READY
                listener.onFailure(error)
            } else try {
                val response = data ?: throw ProtocolFailure("radio_audio_start_missing")
                val rate = response.getInt("rate")
                val newRxStream = unsignedInt(response, "rxStreamId")
                val newTxStream = unsignedInt(response, "txStreamId")
                val credits = response.getInt("txCredits")
                if (rate != RadioHostWire.AUDIO_RATE || newRxStream == newTxStream ||
                    credits !in 0..RadioHostWire.MAX_CREDITS ||
                    response.getString("rxChannel") != rxChannel ||
                    response.getString("txChannel") != txChannel ||
                    response.getString("txPolicy") != "ONE_TX_ONLY")
                    throw ProtocolFailure("radio_audio_start_response")
                synchronized(audioLock) {
                    rxStreamId = newRxStream
                    txStreamId = newTxStream
                    rxSequence = 0
                    rxSample = 0
                    txSequence = 0
                    txSample = 0
                    txCredits = credits
                    audioActive = true
                    audioLock.notifyAll()
                }
                stage = Stage.READY
                listener.onState("radio_audio_ready")
                requestStatus()
            } catch (_: org.json.JSONException) { fail("radio_audio_start_response") }
              catch (failure: ProtocolFailure) { fail(failure.code) }
        })
    }

    fun tune(rxHz: Long, txHz: Long, mode: String, callback: (String?) -> Unit) {
        checkMain()
        if (!authenticated || mode !in setOf("FM", "AM", "USB") ||
            rxHz !in 1..100_000_000_000L || txHz !in 1..100_000_000_000L) {
            callback("radio_tune_invalid")
            return
        }
        if (audioActive) {
            callback("radio_audio_stop_before_tune")
            return
        }
        enqueue(Request("/radio", "set", JSONObject().put("rxHz", rxHz).put("txHz", txHz)
            .put("mode", mode)) { _, error -> callback(error) })
    }

    fun confirmStandaloneProfile(callback: (String?) -> Unit) {
        checkMain()
        if (audioActive) {
            callback("radio_audio_stop_before_profile")
            return
        }
        if (lastStatus?.operationProfile != "STANDALONE_MANUAL") {
            callback("radio_manual_profile_not_available")
            return
        }
        enqueue(Request("/profile", "set", JSONObject()
            .put("profile", "STANDALONE_MANUAL").put("confirm", true)) { data, error ->
            if (error == null && data?.optString("operationProfile") != "STANDALONE_MANUAL")
                callback("radio_profile_confirmation_invalid")
            else callback(error)
        })
    }

    fun setPolarization(value: String, callback: (String?) -> Unit) {
        checkMain()
        if (audioActive) {
            callback("radio_audio_stop_before_polarization")
            return
        }
        if (value !in setOf("LINEAR", "RHCP", "LHCP") ||
            value !in (lastStatus?.polarizationCapabilities ?: emptySet())) {
            callback("radio_polarization_unsupported")
            return
        }
        enqueue(Request("/rf/polarization", "set", JSONObject().put("mode", value)) { _, error ->
            callback(error)
        })
    }

    private var availableChannels = emptySet<String>()

    fun stopAudio(callback: (() -> Unit)? = null) {
        checkMain()
        if (!audioActive) {
            callback?.invoke()
            return
        }
        audioStopping = true
        failTxWaiters()
        enqueue(Request("/audio/stop", "set", JSONObject()) { _, error ->
            clearAudio()
            if (error != null) listener.onFailure(error)
            callback?.invoke()
        })
    }

    fun setPtt(enabled: Boolean, callback: (String?) -> Unit) {
        checkMain()
        if (!audioActive) {
            callback("radio_audio_not_active")
            return
        }
        val body = JSONObject().put("enabled", enabled)
        if (enabled) body.put("leaseMs", 500)
        enqueue(Request("/ptt", "set", body) { _, error -> callback(error) })
    }

    fun sendPcmBlocking(samples: ShortArray, cancelled: () -> Boolean) {
        if (samples.isEmpty()) throw ProtocolFailure("radio_audio_empty_tx")
        var offset = 0
        while (offset < samples.size) {
            if (cancelled() || Thread.currentThread().isInterrupted)
                throw java.util.concurrent.CancellationException()
            val count = minOf(114, samples.size - offset)
            val ids = synchronized(audioLock) {
                val creditDeadline = SystemClock.elapsedRealtime() + 45
                while (audioActive && txCredits == 0 && !cancelled() &&
                    SystemClock.elapsedRealtime() < creditDeadline)
                    audioLock.wait(20)
                if (audioActive && txCredits == 0) throw ProtocolFailure("radio_audio_credit_timeout")
                if (!audioActive || cancelled()) throw ProtocolFailure("radio_audio_stopped")
                txCredits--
                longArrayOf(txStreamId, txSequence, txSample).also {
                    txSequence = (txSequence + 1) and 0xffffffffL
                    txSample = (txSample + count) and 0xffffffffL
                }
            }
            val packet = RadioHostAudioWire.encode(samples, offset, count, mtu, ids[0], ids[1], ids[2])
            writeAudioBlocking(packet)
            offset += count
        }
    }

    private fun writeAudioBlocking(packet: ByteArray) {
        val latch = CountDownLatch(1)
        var result: String? = null
        main.post {
            val connection = gatt
            val characteristic = audioTx
            if (connection == null || characteristic == null || !audioActive || audioWriteActive) {
                result = "radio_audio_write_state"
                latch.countDown()
            } else {
                audioWriteActive = true
                val accepted = if (Build.VERSION.SDK_INT >= 33)
                    connection.writeCharacteristic(characteristic, packet, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT) ==
                        android.bluetooth.BluetoothStatusCodes.SUCCESS
                else {
                    @Suppress("DEPRECATION")
                    characteristic.value = packet
                    characteristic.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
                    @Suppress("DEPRECATION")
                    connection.writeCharacteristic(characteristic)
                }
                if (!accepted) {
                    audioWriteActive = false
                    result = "radio_audio_write_start"
                    latch.countDown()
                } else audioWriteLatch = latch to { error -> result = error }
            }
        }
        if (!latch.await(1500, TimeUnit.MILLISECONDS)) throw ProtocolFailure("radio_audio_write_timeout")
        result?.let { throw ProtocolFailure(it) }
    }

    private var audioWriteLatch: Pair<CountDownLatch, (String?) -> Unit>? = null

    private fun enqueue(request: Request) {
        checkMain()
        if (!authenticated || gatt == null) {
            request.callback(null, "radio_host_not_authenticated")
            return
        }
        if (requestQueue.size >= 16) {
            request.callback(null, "radio_control_queue_full")
            return
        }
        requestQueue.addLast(request)
        sendNextRequest()
    }

    private fun sendNextRequest() {
        if (pendingRequest != null || requestQueue.isEmpty() || gatt == null) return
        val request = requestQueue.removeFirst()
        val id = "a${requestId++}"
        val bytes = try { RadioHostWire.request(id, request.path, request.op, request.data) }
        catch (error: ProtocolFailure) {
            request.callback(null, error.code)
            sendNextRequest()
            return
        }
        val fragments = try { RadioHostWire.controlFrames(bytes, controlSequence) }
        catch (error: ProtocolFailure) {
            request.callback(null, error.code)
            sendNextRequest()
            return
        }
        controlSequence = (controlSequence + 1) and 0xffff
        pendingRequest = request
        pendingId = id
        writeFragments = ArrayDeque(fragments)
        writeNextControlFragment()
    }

    private fun writeNextControlFragment() {
        if (controlWriting || writeFragments.isEmpty()) return
        val connection = gatt ?: return fail("radio_host_disconnected")
        val characteristic = controlTx ?: return fail("radio_host_contract_missing")
        val frame = writeFragments.first
        val accepted = if (Build.VERSION.SDK_INT >= 33)
            connection.writeCharacteristic(characteristic, frame, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT) ==
                android.bluetooth.BluetoothStatusCodes.SUCCESS
        else {
            @Suppress("DEPRECATION")
            characteristic.value = frame
            characteristic.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
            @Suppress("DEPRECATION")
            connection.writeCharacteristic(characteristic)
        }
        if (!accepted) return fail("radio_control_write_start")
        controlWriting = true
        armTimeout()
    }

    private fun receiveControl(bytes: ByteArray) {
        val envelope = try { JSONObject(bytes.toString(Charsets.UTF_8)) }
        catch (_: org.json.JSONException) { throw ProtocolFailure("radio_control_json") }
        if (envelope.optInt("v", -1) != 1) throw ProtocolFailure("radio_control_version")
        val id = envelope.optString("id", "")
        val path = envelope.optString("path", "")
        val data = if (!envelope.has("data") || envelope.isNull("data")) null
            else envelope.optJSONObject("data") ?: throw ProtocolFailure("radio_control_envelope")
        if (id == "event") {
            val eventData = data ?: throw ProtocolFailure("radio_control_envelope")
            when (path) {
                "/audio/credit" -> updateCredits(eventData)
                "/fault" -> {
                    val reason = if (eventData.isNull("reason")) "none" else eventData.optString("reason")
                    clearAudio()
                    listener.onHostEvent(path, eventData)
                    if (reason != "none") listener.onFailure("radio_host_fault_$reason")
                }
                else -> listener.onHostEvent(path, eventData)
            }
            return
        }
        if (id != pendingId || path != pendingRequest?.path) throw ProtocolFailure("radio_control_response_mismatch")
        if (writeFragments.isNotEmpty() || controlWriting) {
            if (completeControlEnvelope != null) throw ProtocolFailure("radio_control_duplicate_response")
            completeControlEnvelope = bytes
            return
        }
        main.removeCallbacks(timeout)
        val ok = envelope.opt("ok") as? Boolean ?: throw ProtocolFailure("radio_control_envelope")
        val rotorRequest = pendingRequest ?: throw ProtocolFailure("radio_control_unsolicited")
        if ((rotorRequest.path to rotorRequest.op) in RotorHostApi.remoteRouteOperations) {
            val (responseData, error) = try {
                RotorHostApi.response(rotorRequest.path, rotorRequest.op, envelope)
            } catch (_: IllegalArgumentException) {
                throw ProtocolFailure("rotor_host_response_schema")
            }
            completeRequest(responseData, error)
            return
        }
        if (!ok) {
            val error = envelope.opt("error") as? String
                ?: throw ProtocolFailure("radio_host_error_missing")
            completeRequest(null, error)
        } else {
            val response = data ?: throw ProtocolFailure("radio_control_envelope")
            when (path) {
                "/auth" -> {
                    if (response.optString("fw") != "radio-host/1.0.0")
                        throw ProtocolFailure("radio_host_version_unsupported")
                    authenticated = true
                    authToken = ""
                    stage = Stage.STATUS
                    completeRequest(response, null)
                }
                "/status" -> {
                    val status = RadioHostStatusParser.parse(response)
                    availableChannels = status.availableChannels
                    lastStatus = status
                    listener.onStatus(status)
                    if (stage == Stage.STATUS) subscribeAudio()
                    completeRequest(response, null)
                }
                "/audio/start" -> completeRequest(response, null)
                else -> completeRequest(response, null)
            }
        }
    }

    private fun completeRequest(data: JSONObject?, error: String?) {
        val request = pendingRequest ?: throw ProtocolFailure("radio_control_unsolicited")
        pendingRequest = null
        pendingId = null
        request.callback(data, error)
        sendNextRequest()
    }

    private fun updateCredits(data: JSONObject) {
        val streamValue = data.opt("txStreamId")
        val eventStream = if (streamValue == null || streamValue == JSONObject.NULL) null
            else (streamValue as? Number)?.toLong()?.and(0xffffffffL)
                ?: throw ProtocolFailure("radio_credit_stream")
        val credits = data.opt("txCredits")
        if (credits !is Number || credits.toInt() !in 0..RadioHostWire.MAX_CREDITS ||
            credits.toDouble() != credits.toInt().toDouble())
            throw ProtocolFailure("radio_credit_value")
        synchronized(audioLock) {
            if (audioActive && eventStream == txStreamId) {
                txCredits = credits.toInt()
                audioLock.notifyAll()
            }
        }
    }

    private fun subscribeAudio() {
        val connection = gatt ?: return fail("radio_host_disconnected")
        val characteristic = audioRx ?: return fail("radio_host_contract_missing")
        stage = Stage.AUDIO_SUBSCRIBE
        if (!connection.setCharacteristicNotification(characteristic, true))
            return fail("radio_audio_notify_enable")
        val descriptor = characteristic.getDescriptor(RadioHostWire.CCCD)
            ?: return fail("radio_audio_cccd_missing")
        val accepted = if (Build.VERSION.SDK_INT >= 33)
            connection.writeDescriptor(descriptor, BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE) ==
                android.bluetooth.BluetoothStatusCodes.SUCCESS
        else {
            @Suppress("DEPRECATION")
            descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            @Suppress("DEPRECATION")
            connection.writeDescriptor(descriptor)
        }
        if (!accepted) fail("radio_audio_subscribe")
        armTimeout()
    }

    private fun requestMtu() {
        val connection = gatt ?: return fail("radio_host_disconnected")
        stage = Stage.MTU
        mtuRetry = false
        if (!connection.requestMtu(247)) fail("radio_mtu_request")
        armTimeout()
    }

    private fun receiveAudio(bytes: ByteArray) {
        if (audioStopping) return
        if (!audioActive) throw ProtocolFailure("radio_audio_inactive_notification")
        val packet = RadioHostAudioWire.parse(bytes, mtu, rxStreamId, rxSequence, rxSample)
        rxSequence = (rxSequence + 1) and 0xffffffffL
        rxSample = (rxSample + packet.samples.size) and 0xffffffffL
        listener.onAudioBlock(PcmBlock(packet.sequence, packet.sampleIndex, packet.samples), rxChannel)
    }

    private fun clearAudio() {
        synchronized(audioLock) {
            audioActive = false
            txCredits = 0
            audioLock.notifyAll()
        }
        audioStopping = false
        rxStreamId = 0; txStreamId = 0; rxSequence = 0; rxSample = 0; txSequence = 0; txSample = 0
    }

    private fun failTxWaiters() {
        synchronized(audioLock) {
            audioActive = false
            txCredits = 0
            audioLock.notifyAll()
        }
    }

    private fun armTimeout() {
        main.removeCallbacks(timeout)
        main.postDelayed(timeout, 15000)
    }

    private fun checkMain() = check(Looper.myLooper() == Looper.getMainLooper())

    private fun fail(code: String) {
        main.removeCallbacks(timeout)
        listener.onFailure(code)
        disconnect(false)
    }

    fun disconnect(report: Boolean = true) {
        if (Looper.myLooper() != Looper.getMainLooper()) {
            main.post { disconnect(report) }
            return
        }
        main.removeCallbacks(timeout)
        clearAudio()
        requestQueue.clear()
        pendingRequest?.callback?.invoke(null, "radio_host_disconnected")
        pendingRequest = null; pendingId = null
        completeControlEnvelope = null
        writeFragments.clear(); controlWriting = false
        controlAssembler.reset()
        authenticated = false; authToken = ""; availableChannels = emptySet()
        audioStopping = false
        stage = Stage.DISCONNECTED
        val previous = gatt
        gatt = null
        controlRx = null; controlTx = null; audioRx = null; audioTx = null
        try { previous?.disconnect() } catch (_: SecurityException) { if (report) listener.onFailure("radio_host_permission") }
        try { previous?.close() } catch (_: SecurityException) { if (report) listener.onFailure("radio_host_permission") }
        if (report) listener.onDisconnected()
    }

    private fun unsignedInt(value: JSONObject, key: String): Long {
        val number = value.opt(key)
        if (number !is Number || number.toDouble() != number.toLong().toDouble())
            throw ProtocolFailure("radio_audio_start_$key")
        return number.toLong().also { if (it !in 0..0xffffffffL) throw ProtocolFailure("radio_audio_start_$key") }
    }

    private val callback = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(source: BluetoothGatt, status: Int, newState: Int) {
            dispatch(source) {
                if (status != BluetoothGatt.GATT_SUCCESS || newState == BluetoothProfile.STATE_DISCONNECTED)
                    fail("radio_host_connection_lost_$status")
                else if (newState == BluetoothProfile.STATE_CONNECTED && stage == Stage.CONNECTING) {
                    stage = Stage.SERVICES
                    if (!source.discoverServices()) fail("radio_host_service_discovery")
                    armTimeout()
                }
            }
        }

        override fun onServicesDiscovered(source: BluetoothGatt, status: Int) {
            dispatch(source) {
                if (stage != Stage.SERVICES) return@dispatch
                if (status != BluetoothGatt.GATT_SUCCESS) return@dispatch fail("radio_host_service_discovery")
                val service = source.getService(RadioHostWire.SERVICE)
                    ?: return@dispatch fail("radio_host_service_missing")
                controlRx = service.getCharacteristic(RadioHostWire.CONTROL_RX)
                controlTx = service.getCharacteristic(RadioHostWire.CONTROL_TX)
                audioRx = service.getCharacteristic(RadioHostWire.AUDIO_RX)
                audioTx = service.getCharacteristic(RadioHostWire.AUDIO_TX)
                if (!validNotify(controlRx) || !validWrite(controlTx) ||
                    !validNotify(audioRx) || !validWrite(audioTx))
                    return@dispatch fail("radio_host_characteristics_invalid")
                subscribeControl()
            }
        }

        override fun onDescriptorWrite(source: BluetoothGatt, descriptor: BluetoothGattDescriptor, status: Int) {
            dispatch(source) {
                if (status != BluetoothGatt.GATT_SUCCESS) return@dispatch fail("radio_host_subscribe_failed")
                when (stage) {
                    Stage.CONTROL_SUBSCRIBE -> {
                        stage = Stage.AUTHENTICATING
                        val data = JSONObject().put("token", authToken)
                        enqueue(Request("/auth", "set", data) { _, error ->
                            if (error != null) fail(error) else requestStatus()
                        })
                    }
                    Stage.AUDIO_SUBSCRIBE -> requestMtu()
                    else -> fail("radio_host_subscription_state")
                }
            }
        }

        override fun onMtuChanged(source: BluetoothGatt, value: Int, status: Int) {
            dispatch(source) {
                if (stage != Stage.MTU) return@dispatch
                if (status != BluetoothGatt.GATT_SUCCESS || value < 247 || value > RadioHostWire.MAX_MTU) {
                    if (!mtuRetry) {
                        mtuRetry = true
                        if (!source.requestMtu(247)) fail("radio_mtu_too_small")
                    } else fail("radio_mtu_too_small")
                    return@dispatch
                }
                mtu = value
                stage = Stage.READY
                main.removeCallbacks(timeout)
                val statusJson = lastStatus ?: return@dispatch fail("radio_status_missing")
                listener.onAudioReady(statusJson.rxChannel, statusJson.txChannel, mtu)
                listener.onState("radio_audio_transport_ready")
            }
        }

        override fun onCharacteristicWrite(
            source: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic,
            status: Int
        ) {
            dispatch(source) {
                if (characteristic.uuid == RadioHostWire.CONTROL_TX && controlWriting) {
                    controlWriting = false
                    if (status != BluetoothGatt.GATT_SUCCESS) return@dispatch fail("radio_control_write_failed")
                    writeFragments.removeFirst()
                    if (writeFragments.isEmpty()) {
                        completeControlEnvelope?.let { complete ->
                            completeControlEnvelope = null
                            receiveControl(complete)
                        }
                    } else writeNextControlFragment()
                } else if (characteristic.uuid == RadioHostWire.AUDIO_TX && audioWriteActive) {
                    audioWriteActive = false
                    val waiter = audioWriteLatch
                    audioWriteLatch = null
                    waiter?.second(if (status == BluetoothGatt.GATT_SUCCESS) null else "radio_audio_write_failed")
                    waiter?.first?.countDown()
                    if (status != BluetoothGatt.GATT_SUCCESS) fail("radio_audio_write_failed")
                }
            }
        }

        @Deprecated("Used on Android 8–12")
        override fun onCharacteristicChanged(source: BluetoothGatt, characteristic: BluetoothGattCharacteristic) {
            if (Build.VERSION.SDK_INT >= 33) return
            @Suppress("DEPRECATION")
            val bytes = characteristic.value?.clone() ?: return
            handleNotification(source, characteristic.uuid, bytes)
        }

        override fun onCharacteristicChanged(
            source: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic,
            value: ByteArray
        ) = handleNotification(source, characteristic.uuid, value.clone())
    }

    private var lastStatus: RadioHostStatus? = null

    private fun subscribeControl() {
        val connection = gatt ?: return fail("radio_host_disconnected")
        val characteristic = controlRx ?: return fail("radio_host_contract_missing")
        stage = Stage.CONTROL_SUBSCRIBE
        if (!connection.setCharacteristicNotification(characteristic, true))
            return fail("radio_control_notify_enable")
        val descriptor = characteristic.getDescriptor(RadioHostWire.CCCD)
            ?: return fail("radio_control_cccd_missing")
        val accepted = if (Build.VERSION.SDK_INT >= 33)
            connection.writeDescriptor(descriptor, BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE) ==
                android.bluetooth.BluetoothStatusCodes.SUCCESS
        else {
            @Suppress("DEPRECATION")
            descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            @Suppress("DEPRECATION")
            connection.writeDescriptor(descriptor)
        }
        if (!accepted) fail("radio_control_subscribe")
        armTimeout()
    }

    private fun validNotify(value: BluetoothGattCharacteristic?): Boolean =
        value != null && value.properties and BluetoothGattCharacteristic.PROPERTY_NOTIFY != 0 &&
            value.properties and BluetoothGattCharacteristic.PROPERTY_READ != 0

    private fun validWrite(value: BluetoothGattCharacteristic?): Boolean =
        value != null && value.properties and BluetoothGattCharacteristic.PROPERTY_WRITE != 0

    private fun dispatch(source: BluetoothGatt, action: () -> Unit) {
        main.post {
            if (source !== gatt) return@post
            try { action() }
            catch (_: SecurityException) { fail("radio_host_permission") }
            catch (failure: ProtocolFailure) { fail(failure.code) }
            catch (_: org.json.JSONException) { fail("radio_host_json") }
        }
    }

    private fun handleNotification(source: BluetoothGatt, uuid: UUID, bytes: ByteArray) {
        dispatch(source) {
            when (uuid) {
                RadioHostWire.CONTROL_RX -> {
                    val complete = controlAssembler.feed(bytes)
                    if (complete != null) receiveControl(complete)
                }
                RadioHostWire.AUDIO_RX -> receiveAudio(bytes)
            }
        }
    }
}
