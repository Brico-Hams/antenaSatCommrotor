package org.bricohams.portablesatstation

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.media.AudioAttributes
import android.media.AudioDeviceInfo
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.AudioTrack
import android.media.MediaRecorder
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import android.text.InputType
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.Spinner
import android.widget.TextView
import org.bricohams.portablesatstation.orbit.SatelliteOverviewView
import java.io.IOException
import java.util.Locale
import java.util.concurrent.ArrayBlockingQueue
import java.util.concurrent.CancellationException
import java.util.concurrent.Executors
import java.util.concurrent.Future

internal class RadioHostActivity : Activity(), RadioHostBleTransport.Listener {
    private data class MicInput(val device: AudioDeviceInfo, val label: String)
    private enum class DecodeMode { PD120, PD180, AX25 }

    private val main = Handler(Looper.getMainLooper())
    private val worker = Executors.newSingleThreadExecutor()
    private lateinit var transport: RadioHostBleTransport
    private lateinit var token: EditText
    private lateinit var statusView: TextView
    private lateinit var channelRx: Spinner
    private lateinit var channelTx: Spinner
    private lateinit var mode: Spinner
    private lateinit var rxHz: EditText
    private lateinit var txHz: EditText
    private lateinit var decodeMode: Spinner
    private lateinit var ownCall: EditText
    private lateinit var recipient: EditText
    private lateinit var messageBody: EditText
    private lateinit var messageId: EditText
    private lateinit var path: EditText
    private lateinit var localArm: CheckBox
    private lateinit var micPicker: Spinner
    private lateinit var decodeButton: Button
    private lateinit var saveImageButton: Button
    private lateinit var saveLogButton: Button
    private lateinit var imageView: ImageView
    private lateinit var resultView: TextView
    private lateinit var profileButton: Button
    private lateinit var polarizationButton: Button
    private lateinit var transmitMessageButton: Button
    private lateinit var voiceButton: Button
    private lateinit var stopTransmitButton: Button
    private lateinit var monitorButton: Button
    private lateinit var orbitOverview: SatelliteOverviewView
    private val aprsWatchers = mutableListOf<TextWatcher>()
    private var bondedDevices = emptyList<BluetoothDevice>()
    private var micInputs = emptyList<MicInput>()
    private var currentStatus: RadioHostStatus? = null
    private var statusReceivedAt = 0L
    private var radioChannels = emptyList<String>()
    private var capture: RadioPcmCapture? = null
    private var decodedBitmap: Bitmap? = null
    private var packetLog: String? = null
    private var preparedFrame: ByteArray? = null
    private var preparedAudio: ShortArray? = null
    private var txTask: Future<*>? = null
    private var activeRecorder: AudioRecord? = null
    private val playbackQueue = ArrayBlockingQueue<ShortArray>(16)
    @Volatile private var monitoringVoice = false
    @Volatile private var activeTrack: AudioTrack? = null
    private var playbackTask: Future<*>? = null
    @Volatile private var txCancelled = true
    @Volatile private var shuttingDown = false
    private var manualProfileConfirmed = false
    private var txGeneration = 0
    private var txChannelForLease = ""
    private val txControlsRefresh = object : Runnable {
        override fun run() {
            refreshTxControls()
            main.postDelayed(this, TX_CONTROLS_REFRESH_MS)
        }
    }
    private val txStatusRefresh = object : Runnable {
        override fun run() {
            if (txCancelled) return
            transport.requestStatus { _, error ->
                if (error != null) stopTransmit(error)
                else if (!txCancelled) main.postDelayed(this, TX_STATUS_REFRESH_MS)
            }
        }
    }
    private val txTimeout = Runnable { stopTransmit("radio_tx_duration_limit") }
    private var leaseRenewal = object : Runnable {
        override fun run() {
            if (txCancelled || !transport.readyForAudio || !txInterlocksMaintainable()) {
                stopTransmit("radio_tx_interlock_changed")
                return
            }
            transport.setPtt(true) { error ->
                if (error != null) stopTransmit(error)
                else if (!txCancelled) main.postDelayed(this, LEASE_RENEWAL_MS)
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        transport = RadioHostBleTransport(this, this)
        buildScreen()
        ownCall.setText(getSharedPreferences(APRS_PREFS, MODE_PRIVATE).getString("station_call", ""))
        if (hasBluetoothPermission()) refreshBondedDevices()
        else statusView.setText(R.string.radio_permission_prompt)
        refreshMicInputs()
    }

    override fun onStart() {
        super.onStart()
        main.removeCallbacks(txControlsRefresh)
        main.post(txControlsRefresh)
    }

    private fun buildScreen() {
        val column = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(24, 16, 24, 24)
        }
        setContentView(ScrollView(this).apply { addView(column) })
        Branding.header(this, column, Branding.Topic.RADIO)
        text(column, getString(R.string.radio_title), 22f)
        text(column, getString(R.string.radio_disclosure), 14f)
        button(column, R.string.digital_back) { safeShutdown(finishActivity = true) }
        statusView = text(column, getString(R.string.radio_disconnected), 16f).apply {
            accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_POLITE
        }
        token = input(column, R.string.radio_token, password = true)
        button(column, R.string.radio_refresh_bonded) { refreshBondedDevices() }
        button(column, R.string.radio_connect) { chooseBondedDevice() }
        button(column, R.string.radio_disconnect) { safeShutdown() }
        button(column, R.string.radio_status) {
            if (transport.connectedAndAuthenticated) transport.requestStatus()
            else statusView.setText(R.string.radio_not_authenticated)
        }

        text(column, getString(R.string.radio_channels_heading), 18f)
        text(column, getString(R.string.radio_rx_channel), 14f)
        channelRx = Spinner(this).also { column.addView(it) }
        text(column, getString(R.string.radio_tx_channel), 14f)
        channelTx = Spinner(this).also { column.addView(it) }
        channelTx.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                refreshTxControls()
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {
                refreshTxControls()
            }
        }
        text(column, getString(R.string.radio_tune_heading), 18f)
        rxHz = input(column, R.string.radio_rx_hz)
        txHz = input(column, R.string.radio_tx_hz)
        mode = Spinner(this).apply {
            adapter = ArrayAdapter(this@RadioHostActivity,
                android.R.layout.simple_spinner_dropdown_item,
                arrayOf("FM", "AM", "USB"))
            column.addView(this)
        }
        button(column, R.string.radio_tune) { tuneRadio() }
        profileButton = button(column, R.string.radio_confirm_manual) {
            confirmManualProfile()
        }.apply { isEnabled = false }
        polarizationButton = button(column, R.string.radio_set_polarization) {
            choosePolarization()
        }.apply { isEnabled = false }
        button(column, R.string.radio_start_audio) { startAudio() }
        decodeMode = Spinner(this).apply {
            adapter = ArrayAdapter(this@RadioHostActivity,
                android.R.layout.simple_spinner_dropdown_item,
                resources.getStringArray(R.array.digital_modes))
            column.addView(this)
        }
        decodeButton = button(column, R.string.radio_stop_decode) { stopAudioAndDecode() }
            .apply { isEnabled = false }
        monitorButton = button(column, R.string.radio_voice_monitor) { toggleVoiceMonitor() }
            .apply { isEnabled = false }
        saveImageButton = button(column, R.string.sstv_save_image) { saveResult(IMAGE_REQUEST) }
            .apply { isEnabled = false }
        saveLogButton = button(column, R.string.ax25_save_log) { saveResult(LOG_REQUEST) }
            .apply { isEnabled = false }
        imageView = ImageView(this).apply {
            adjustViewBounds = true
            scaleType = ImageView.ScaleType.FIT_CENTER
            contentDescription = getString(R.string.sstv_image_description)
        }
        column.addView(imageView)
        resultView = text(column, getString(R.string.radio_no_result), 14f)

        text(column, getString(R.string.radio_aprs_heading), 18f)
        ownCall = input(column, R.string.aprs_station_call)
        recipient = input(column, R.string.aprs_recipient)
        messageBody = input(column, R.string.aprs_message_body)
        messageId = input(column, R.string.aprs_message_id)
        path = input(column, R.string.aprs_digipeater_path)
        listOf(ownCall, recipient, messageBody, messageId, path).forEach { field ->
            val watcher = object : TextWatcher {
                override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
                override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) = Unit
                override fun afterTextChanged(s: Editable?) {
                    preparedAudio = null
                    preparedFrame = null
                    refreshTxControls()
                }
            }
            field.addTextChangedListener(watcher)
            aprsWatchers.add(watcher)
        }
        localArm = CheckBox(this).apply {
            setText(R.string.radio_local_tx_confirmation)
            isChecked = false
            setOnCheckedChangeListener { _, checked ->
                if (!checked) {
                    preparedAudio = null
                    preparedFrame = null
                    refreshTxControls()
                    if (!txCancelled) stopTransmit("radio_local_arm_released")
                }
            }
            column.addView(this)
        }
        button(column, R.string.radio_prepare_aprs) { prepareAprsMessage() }
        transmitMessageButton = button(column, R.string.radio_send_aprs) {
            confirmAndSendPreparedMessage()
        }.apply { isEnabled = false }

        text(column, getString(R.string.radio_voice_heading), 18f)
        text(column, getString(R.string.radio_mic_disclosure), 14f)
        micPicker = Spinner(this).also { column.addView(it) }
        button(column, R.string.audio_refresh_inputs) { refreshMicInputs() }
        voiceButton = button(column, R.string.radio_voice_tx) { requestMicrophonePermission() }
            .apply { isEnabled = false }
        stopTransmitButton = button(column, R.string.radio_stop_tx) { stopTransmit(null) }
            .apply { isEnabled = false }
        orbitOverview = SatelliteOverviewView(this).apply {
            submitSnapshot(null)
            onHostRouteRequested = { route, operation, data ->
                if (!transport.connectedAndAuthenticated) {
                    submitHostRouteResult(route, null, "radio_host_not_authenticated")
                } else {
                    transport.requestRotorHost(route, operation, data) { response, error ->
                        submitHostRouteResult(route, response, error)
                    }
                }
            }
        }
        column.addView(orbitOverview)
    }

    private fun text(parent: LinearLayout, value: String, size: Float): TextView =
        TextView(this).apply {
            text = value
            textSize = size
            setPadding(0, 8, 0, 8)
            parent.addView(this)
        }

    private fun button(parent: LinearLayout, label: Int, action: () -> Unit): Button =
        Button(this).apply {
            setText(label)
            setOnClickListener { action() }
            parent.addView(this)
        }

    private fun input(parent: LinearLayout, hint: Int, password: Boolean = false): EditText =
        EditText(this).apply {
            setHint(hint)
            setSingleLine(true)
            inputType = if (password) InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            else InputType.TYPE_CLASS_TEXT
            parent.addView(this)
        }

    private fun refreshBondedDevices() {
        if (!hasBluetoothPermission()) {
            requestBluetoothPermission()
            return
        }
        try {
            val adapter = (getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager).adapter
            bondedDevices = adapter?.bondedDevices?.sortedBy { it.name.orEmpty() } ?: emptyList()
            statusView.setText(if (bondedDevices.isEmpty()) R.string.radio_no_bonded_devices
                else R.string.radio_choose_bonded_device)
        } catch (_: SecurityException) {
            statusView.setText(R.string.radio_permission_denied)
        }
    }

    private fun chooseBondedDevice() {
        if (!hasBluetoothPermission()) {
            requestBluetoothPermission()
            return
        }
        val credential = token.text.toString().trim()
        if (!credential.matches(Regex("[0-9a-fA-F]{64}"))) {
            statusView.setText(R.string.radio_token_invalid)
            return
        }
        refreshBondedDevices()
        if (bondedDevices.isEmpty()) return
        val labels = try {
            bondedDevices.map { "${it.name ?: getString(R.string.radio_unknown_device)} · ${it.address}" }
        } catch (_: SecurityException) {
            statusView.setText(R.string.radio_permission_denied)
            return
        }
        AlertDialog.Builder(this)
            .setTitle(R.string.radio_select_host)
            .setItems(labels.toTypedArray()) { _, index ->
                val device = bondedDevices.getOrNull(index) ?: return@setItems
                try {
                    if (device.bondState != BluetoothDevice.BOND_BONDED) {
                        statusView.setText(R.string.radio_bond_required)
                        return@setItems
                    }
                    shuttingDown = false
                    manualProfileConfirmed = false
                    currentStatus = null
                    statusReceivedAt = 0
                    transport.connect(device, credential)
                } catch (_: SecurityException) {
                    statusView.setText(R.string.radio_permission_denied)
                }
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun hasBluetoothPermission(): Boolean =
        Build.VERSION.SDK_INT < 31 ||
            checkSelfPermission(Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED

    private fun requestBluetoothPermission() {
        if (Build.VERSION.SDK_INT >= 31)
            requestPermissions(arrayOf(Manifest.permission.BLUETOOTH_CONNECT), REQUEST_BLUETOOTH)
        else statusView.setText(R.string.radio_permission_denied)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        when (requestCode) {
            REQUEST_BLUETOOTH -> if (grantResults.firstOrNull() == PackageManager.PERMISSION_GRANTED)
                refreshBondedDevices() else statusView.setText(R.string.radio_permission_denied)
            REQUEST_MICROPHONE -> if (grantResults.firstOrNull() == PackageManager.PERMISSION_GRANTED)
                confirmVoiceTransmit() else statusView.setText(R.string.audio_permission_denied)
        }
    }

    private fun refreshMicInputs() {
        val manager = getSystemService(Context.AUDIO_SERVICE) as android.media.AudioManager
        micInputs = manager.getDevices(android.media.AudioManager.GET_DEVICES_INPUTS)
            .filter {
                it.type == AudioDeviceInfo.TYPE_BUILTIN_MIC ||
                    it.type == AudioDeviceInfo.TYPE_USB_DEVICE ||
                    it.type == AudioDeviceInfo.TYPE_USB_HEADSET ||
                    it.type == AudioDeviceInfo.TYPE_WIRED_HEADSET
            }
            .map { device ->
                val description = device.productName?.toString()?.takeIf { it.isNotBlank() }
                    ?: getString(R.string.radio_unknown_microphone)
                MicInput(device, description)
            }
        micPicker.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item,
            micInputs.map { it.label })
        voiceButton.isEnabled = micInputs.isNotEmpty() && transport.readyForAudio
    }

    private fun tuneRadio() {
        val rx = rxHz.text.toString().trim().toLongOrNull()
        val tx = txHz.text.toString().trim().toLongOrNull()
        if (rx == null || tx == null) {
            statusView.setText(R.string.radio_frequency_invalid)
            return
        }
        val rxChannelExpected = frequencyChannel(rx)
        val txChannelExpected = frequencyChannel(tx)
        val live = currentStatus
        if (rxChannelExpected == null || txChannelExpected == null || live == null ||
            rxChannelExpected != live.rxChannel || txChannelExpected != live.txChannel) {
            statusView.setText(R.string.radio_frequency_channel_mismatch)
            return
        }
        val selectedMode = mode.selectedItem?.toString() ?: return
        transport.tune(rx, tx, selectedMode) { error ->
            if (error != null) onFailure(error)
            else {
                statusView.setText(R.string.radio_tune_accepted)
                transport.requestStatus()
            }
        }
    }

    private fun confirmManualProfile() {
        if (currentStatus?.operationProfile != "STANDALONE_MANUAL") return
        AlertDialog.Builder(this)
            .setMessage(R.string.radio_manual_profile_warning)
            .setPositiveButton(R.string.confirm) { _, _ ->
                transport.confirmStandaloneProfile { error ->
                    if (error != null) onFailure(error)
                    else {
                        manualProfileConfirmed = true
                        statusView.setText(R.string.radio_manual_profile_confirmed)
                        transport.requestStatus()
                    }
                }
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun choosePolarization() {
        val capabilities = currentStatus?.polarizationCapabilities?.sorted().orEmpty()
        if (capabilities.isEmpty()) {
            statusView.setText(R.string.radio_polarization_unavailable)
            return
        }
        AlertDialog.Builder(this)
            .setTitle(R.string.radio_polarization_title)
            .setItems(capabilities.toTypedArray()) { _, index ->
                val selected = capabilities.getOrNull(index) ?: return@setItems
                AlertDialog.Builder(this)
                    .setMessage(R.string.radio_polarization_warning)
                    .setPositiveButton(R.string.confirm) { _, _ ->
                        transport.setPolarization(selected) { error ->
                            if (error != null) onFailure(error)
                            else {
                                statusView.setText(R.string.radio_polarization_requested)
                                transport.requestStatus()
                            }
                        }
                    }
                    .setNegativeButton(R.string.cancel, null)
                    .show()
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun startAudio() {
        if (!transport.connectedAndAuthenticated) {
            statusView.setText(R.string.radio_not_authenticated)
            return
        }
        val rx = radioChannels.getOrNull(channelRx.selectedItemPosition)
        val tx = radioChannels.getOrNull(channelTx.selectedItemPosition)
        if (rx == null || tx == null) {
            statusView.setText(R.string.radio_no_channels)
            return
        }
        if (radioChannels.size > 1 && rx == tx) {
            statusView.setText(R.string.radio_crossband_required)
            return
        }
        clearResult()
        capture = RadioPcmCapture()
        decodeButton.isEnabled = false
        channelRx.isEnabled = false
        channelTx.isEnabled = false
        statusView.setText(R.string.radio_audio_starting)
        transport.startAudio(rx, tx)
    }

    private fun stopAudioAndDecode() {
        val current = capture ?: return
        decodeButton.isEnabled = false
        stopVoiceMonitor()
        stopTransmit(null)
        transport.stopAudio {
            channelRx.isEnabled = true
            channelTx.isEnabled = true
            if (current.failed) {
                capture = null
                statusView.setText(R.string.radio_capture_invalid)
            } else decodeCapture(current)
        }
    }

    private fun toggleVoiceMonitor() {
        if (monitoringVoice) {
            stopVoiceMonitor()
            return
        }
        if (!transport.readyForAudio) {
            statusView.setText(R.string.radio_audio_not_ready)
            return
        }
        playbackQueue.clear()
        monitoringVoice = true
        monitorButton.setText(R.string.radio_voice_monitor_stop)
        playbackTask = worker.submit {
            var track: AudioTrack? = null
            try {
                val minimum = AudioTrack.getMinBufferSize(
                    SAMPLE_RATE, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT
                )
                if (minimum <= 0) throw ProtocolFailure("radio_voice_playback_unavailable")
                track = AudioTrack.Builder()
                    .setAudioAttributes(AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_MEDIA)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build())
                    .setAudioFormat(AudioFormat.Builder().setSampleRate(SAMPLE_RATE)
                        .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                        .setEncoding(AudioFormat.ENCODING_PCM_16BIT).build())
                    .setBufferSizeInBytes(maxOf(minimum * 2, SAMPLE_RATE / 2))
                    .setTransferMode(AudioTrack.MODE_STREAM)
                    .build()
                if (track.state != AudioTrack.STATE_INITIALIZED)
                    throw ProtocolFailure("radio_voice_playback_unavailable")
                activeTrack = track
                track.play()
                main.post { statusView.setText(R.string.radio_voice_monitor_active) }
                while (monitoringVoice && !Thread.currentThread().isInterrupted) {
                    val samples = playbackQueue.poll(100, java.util.concurrent.TimeUnit.MILLISECONDS) ?: continue
                    var offset = 0
                    while (monitoringVoice && offset < samples.size) {
                        val written = track.write(samples, offset, samples.size - offset, AudioTrack.WRITE_BLOCKING)
                        if (written <= 0) throw ProtocolFailure("radio_voice_playback_write")
                        offset += written
                    }
                }
            } catch (_: InterruptedException) {
                Thread.currentThread().interrupt()
            } catch (failure: ProtocolFailure) {
                main.post {
                    if (monitoringVoice) {
                        stopVoiceMonitor()
                        statusView.text = getString(R.string.radio_voice_monitor_failed, failure.code)
                    }
                }
            } finally {
                track?.let {
                    try { if (it.playState == AudioTrack.PLAYSTATE_PLAYING) it.stop() }
                    catch (_: IllegalStateException) { }
                    it.release()
                }
                if (activeTrack === track) activeTrack = null
            }
        }
    }

    private fun stopVoiceMonitor() {
        monitoringVoice = false
        playbackQueue.clear()
        try {
            activeTrack?.let {
                if (it.playState == AudioTrack.PLAYSTATE_PLAYING) it.stop()
            }
        } catch (_: IllegalStateException) {
            statusView.text = getString(R.string.radio_voice_monitor_failed, "audio_track_stop")
        }
        playbackTask?.cancel(true)
        playbackTask = null
        if (::monitorButton.isInitialized) {
            monitorButton.setText(R.string.radio_voice_monitor)
            monitorButton.isEnabled = false
        }
    }

    private fun decodeCapture(audio: RadioPcmCapture) {
        val modeAtStart = when (decodeMode.selectedItemPosition) {
            0 -> DecodeMode.PD120
            1 -> DecodeMode.PD180
            2 -> DecodeMode.AX25
            else -> {
                statusView.setText(R.string.radio_decode_mode_invalid)
                return
            }
        }
        val own = ownCall.text.toString()
        statusView.setText(R.string.audio_decoding)
        worker.submit {
            try {
                val samples = audio.snapshot()
                if (samples.size < SAMPLE_RATE / 10) throw ProtocolFailure("audio_too_short")
                when (modeAtStart) {
                    DecodeMode.PD120, DecodeMode.PD180 -> {
                        val choice = if (modeAtStart == DecodeMode.PD120)
                            SstvModeChoice.PD120 else SstvModeChoice.PD180
                        val decoded = SstvDecoder.decode(samples, SAMPLE_RATE, choice) {
                            Thread.currentThread().isInterrupted
                        }
                        val bitmap = Bitmap.createBitmap(decoded.pixels, decoded.mode.width,
                            decoded.mode.height, Bitmap.Config.ARGB_8888)
                        main.post {
                            decodedBitmap = bitmap
                            packetLog = null
                            imageView.setImageBitmap(bitmap)
                            resultView.text = getString(R.string.sstv_decoded, decoded.mode.name,
                                decoded.mode.width, decoded.mode.height, decoded.verifiedLines)
                            saveImageButton.isEnabled = true
                            saveLogButton.isEnabled = false
                            statusView.setText(R.string.radio_decode_complete)
                        }
                    }
                    DecodeMode.AX25 -> {
                        val packets = Ax25AfskDecoder.decode(samples, SAMPLE_RATE) {
                            Thread.currentThread().isInterrupted
                        }
                        val log = packets.joinToString("\n\n") { it.logEntry() }
                        val inbox = AprsInbox.addressedTo(packets, own)
                        main.post {
                            decodedBitmap = null
                            packetLog = log
                            imageView.setImageDrawable(null)
                            resultView.text = buildString {
                                append(getString(R.string.ax25_decoded, packets.size, log))
                                append("\n\n")
                                append(getString(R.string.aprs_inbox_title))
                                append('\n')
                                append(if (inbox.isEmpty()) getString(R.string.aprs_inbox_empty)
                                    else inbox.joinToString("\n\n"))
                            }
                            saveImageButton.isEnabled = false
                            saveLogButton.isEnabled = true
                            statusView.setText(R.string.radio_decode_complete)
                        }
                    }
                }
            } catch (failure: ProtocolFailure) {
                main.post { statusView.text = getString(R.string.digital_decode_failed, failure.code) }
            } catch (_: CancellationException) {
                main.post { statusView.setText(R.string.audio_cancelled) }
            }
        }
    }

    private fun prepareAprsMessage() {
        try {
            if (!localArm.isChecked) throw ProtocolFailure("aprs_plaintext_not_confirmed")
            val source = AprsAddressing.normalizeCallsign(ownCall.text.toString())
                ?: throw ProtocolFailure("aprs_source_invalid")
            val destination = AprsAddressing.normalizeCallsign(recipient.text.toString())
                ?: throw ProtocolFailure("aprs_destination_invalid")
            val digis = AprsAddressing.parsePath(path.text.toString())
                ?: throw ProtocolFailure("aprs_path_invalid")
            val id = messageId.text.toString().trim().ifEmpty { null }
            val information = AprsMessageCodec.encodeMessageInformation(
                destination, messageBody.text.toString(), id
            )
            val frame = AprsMessageCodec.encodeUiFrame(source, "APRS", digis, information)
            preparedFrame = frame
            preparedAudio = Bell202Encoder.encode(frame).samples
            getSharedPreferences(APRS_PREFS, MODE_PRIVATE).edit().putString("station_call", source).apply()
            refreshTxControls()
            statusView.setText(R.string.radio_aprs_prepared)
        } catch (error: ProtocolFailure) {
            preparedFrame = null
            preparedAudio = null
            refreshTxControls()
            statusView.text = getString(R.string.digital_decode_failed, error.code)
        }
    }

    private fun confirmAndSendPreparedMessage() {
        prepareAprsMessage()
        if (preparedAudio == null || preparedFrame == null) {
            statusView.setText(R.string.radio_aprs_not_prepared)
            return
        }
        val live = currentStatus
        if (!localArm.isChecked || live == null ||
            SystemClock.elapsedRealtime() - statusReceivedAt > STATUS_MAX_AGE_MS ||
            !live.canRequestPtt(channelTx.selectedItem?.toString().orEmpty()) ||
            (live.operationProfile == "STANDALONE_MANUAL" && !manualProfileConfirmed)) {
            statusView.setText(R.string.radio_tx_interlock_blocked)
            return
        }
        if (live.mode != "FM") {
            statusView.setText(R.string.radio_aprs_requires_fm)
            return
        }
        AlertDialog.Builder(this)
            .setMessage(R.string.radio_aprs_tx_warning)
            .setPositiveButton(R.string.confirm) { _, _ ->
                if (!txInterlocksOkay() || currentStatus?.mode != "FM")
                    statusView.setText(R.string.radio_tx_interlock_blocked)
                else preparedAudio?.clone()?.let { startTransmit(it, null) }
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun requestMicrophonePermission() {
        if (!transport.readyForAudio || micInputs.isEmpty()) {
            statusView.setText(R.string.radio_audio_not_ready)
            return
        }
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED)
            confirmVoiceTransmit()
        else AlertDialog.Builder(this)
            .setMessage(R.string.radio_mic_permission_explanation)
            .setPositiveButton(R.string.confirm) { _, _ ->
                requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), REQUEST_MICROPHONE)
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun confirmVoiceTransmit() {
        if (!txInterlocksOkay()) {
            statusView.setText(R.string.radio_tx_interlock_blocked)
            return
        }
        AlertDialog.Builder(this)
            .setMessage(R.string.radio_voice_tx_warning)
            .setPositiveButton(R.string.confirm) { _, _ -> startTransmit(null, micInputs.getOrNull(micPicker.selectedItemPosition)) }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun txInterlocksOkay(): Boolean {
        val live = currentStatus ?: return false
        return localArm.isChecked && SystemClock.elapsedRealtime() - statusReceivedAt <= STATUS_MAX_AGE_MS &&
            live.canRequestPtt(channelTx.selectedItem?.toString().orEmpty()) &&
            (live.operationProfile != "STANDALONE_MANUAL" || manualProfileConfirmed)
    }

    private fun txInterlocksMaintainable(): Boolean {
        val live = currentStatus ?: return false
        return localArm.isChecked && SystemClock.elapsedRealtime() - statusReceivedAt <= STATUS_MAX_AGE_MS &&
            live.canMaintainPtt(txChannelForLease) &&
            (live.operationProfile != "STANDALONE_MANUAL" || manualProfileConfirmed)
    }

    private fun frequencyChannel(hz: Long): String? = RadioHostWire.channelForFrequency(hz)

    private fun startTransmit(samples: ShortArray?, microphone: MicInput?) {
        if (!txInterlocksOkay() || !transport.readyForAudio || txTask?.isDone == false) {
            statusView.setText(R.string.radio_tx_interlock_blocked)
            return
        }
        txCancelled = false
        txGeneration++
        val generation = txGeneration
        txChannelForLease = channelTx.selectedItem?.toString().orEmpty()
        refreshTxControls()
        statusView.setText(R.string.radio_tx_requesting_lease)
        transport.setPtt(true) { error ->
            if (error != null) {
                stopTransmit(error)
                return@setPtt
            }
            statusView.setText(R.string.radio_tx_audio_active)
            main.postDelayed(leaseRenewal, LEASE_RENEWAL_MS)
            main.postDelayed(txStatusRefresh, TX_STATUS_REFRESH_MS)
            main.postDelayed(txTimeout, MAX_TX_DURATION_MS)
            txTask = worker.submit {
                try {
                    if (samples != null) {
                        transport.sendPcmBlocking(samples) { txCancelled || generation != txGeneration }
                    } else {
                        val source = microphone ?: throw ProtocolFailure("radio_microphone_unavailable")
                        streamMicrophone(source, generation)
                    }

                    main.post {
                        if (generation == txGeneration && !txCancelled) {
                            stopTransmit(null)
                            statusView.setText(R.string.radio_tx_audio_accepted)
                        }
                    }
                } catch (_: CancellationException) {
                    Unit
                } catch (_: InterruptedException) {
                    Thread.currentThread().interrupt()
                } catch (failure: ProtocolFailure) {
                    main.post { if (generation == txGeneration) stopTransmit(failure.code) }
                } catch (_: SecurityException) {
                    main.post { if (generation == txGeneration) stopTransmit("radio_microphone_permission") }
                } catch (_: IllegalStateException) {
                    main.post { if (generation == txGeneration) stopTransmit("radio_microphone_failed") }
                } finally {
                    activeRecorder?.let { recorder ->
                        try { if (recorder.recordingState == AudioRecord.RECORDSTATE_RECORDING) recorder.stop() }
                        catch (_: IllegalStateException) { }
                        recorder.release()
                        activeRecorder = null
                    }
                }
            }
        }
    }

    private fun streamMicrophone(input: MicInput, generation: Int) {
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED)
            throw ProtocolFailure("radio_microphone_permission")
        val minimum = AudioRecord.getMinBufferSize(SAMPLE_RATE, AudioFormat.CHANNEL_IN_MONO,
            AudioFormat.ENCODING_PCM_16BIT)
        if (minimum <= 0) throw ProtocolFailure("radio_microphone_unavailable")
        val recorder = try {
            AudioRecord.Builder()
                .setAudioSource(MediaRecorder.AudioSource.MIC)
                .setAudioFormat(AudioFormat.Builder().setSampleRate(SAMPLE_RATE)
                    .setChannelMask(AudioFormat.CHANNEL_IN_MONO)
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT).build())
                .setBufferSizeInBytes(maxOf(minimum * 2, SAMPLE_RATE / 2))
                .build()
        } catch (_: IllegalArgumentException) {
            throw ProtocolFailure("radio_microphone_unavailable")
        }
        if (recorder.state != AudioRecord.STATE_INITIALIZED) {
            recorder.release()
            throw ProtocolFailure("radio_microphone_unavailable")
        }
        if (!recorder.setPreferredDevice(input.device)) {
            recorder.release()
            throw ProtocolFailure("radio_microphone_route")
        }
        activeRecorder = recorder
        recorder.startRecording()
        val routeDeadline = android.os.SystemClock.elapsedRealtime() + 2000
        var routed = recorder.routedDevice
        while (!txCancelled && generation == txGeneration &&
            (routed == null || routed.id != input.device.id) &&
            android.os.SystemClock.elapsedRealtime() < routeDeadline) {
            Thread.sleep(40)
            routed = recorder.routedDevice
        }
        if (txCancelled || generation != txGeneration) throw CancellationException()
        if (routed == null || routed.id != input.device.id)
            throw ProtocolFailure("radio_microphone_route")
        val block = ShortArray(114)
        while (!txCancelled && generation == txGeneration) {
            val count = recorder.read(block, 0, block.size, AudioRecord.READ_BLOCKING)
            if (count <= 0) throw ProtocolFailure("radio_microphone_read")
            transport.sendPcmBlocking(block.copyOf(count)) {
                txCancelled || generation != txGeneration
            }
        }
    }

    private fun stopTransmit(error: String?) {
        if (txCancelled) return
        txCancelled = true
        main.removeCallbacks(leaseRenewal)
        main.removeCallbacks(txStatusRefresh)
        main.removeCallbacks(txTimeout)
        txTask?.cancel(true)
        try {
            activeRecorder?.let {
                if (it.recordingState == AudioRecord.RECORDSTATE_RECORDING) it.stop()
            }
        } catch (_: IllegalStateException) {
            if (error == null) statusView.setText(R.string.radio_microphone_failed)
        }
        if (transport.readyForAudio) transport.setPtt(false) { releaseError ->
            if (releaseError != null) statusView.text = getString(R.string.radio_tx_release_failed, releaseError)
        }
        refreshTxControls()
        if (error != null) {
            statusView.text = when (error) {
                "radio_tx_interlock_changed" -> getString(R.string.radio_tx_interlock_changed)
                "radio_local_arm_released" -> getString(R.string.radio_local_arm_released)
                else -> getString(R.string.radio_tx_failed, error)
            }
        }
    }

    private fun refreshTxControls() {
        if (!::transmitMessageButton.isInitialized || !::voiceButton.isInitialized) return
        val statusAge = SystemClock.elapsedRealtime() - statusReceivedAt
        if (currentStatus != null && statusAge > STATUS_MAX_AGE_MS) {
            statusView.setText(R.string.radio_tx_status_stale)
        }
        val eligible = !shuttingDown && txCancelled && transport.readyForAudio && txInterlocksOkay()
        transmitMessageButton.isEnabled = eligible && preparedAudio != null &&
            currentStatus?.mode == "FM"
        voiceButton.isEnabled = eligible && micInputs.isNotEmpty()
        stopTransmitButton.isEnabled = !txCancelled
    }

    private fun onAudioCaptureFailure(code: String) {
        capture?.failed = true
        stopVoiceMonitor()
        transport.stopAudio()
        decodeButton.isEnabled = false
        statusView.text = getString(R.string.radio_capture_failed, code)
    }

    private fun clearResult() {
        decodedBitmap = null
        packetLog = null
        imageView.setImageDrawable(null)
        resultView.setText(R.string.radio_no_result)
        saveImageButton.isEnabled = false
        saveLogButton.isEnabled = false
    }

    private fun saveResult(request: Int) {
        val image = request == IMAGE_REQUEST
        if (image && decodedBitmap == null || !image && packetLog == null) return
        val title = if (image) "PortableSatStation-SSTV.png" else "PortableSatStation-AX25-APRS.txt"
        startActivityForResult(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            type = if (image) "image/png" else "text/plain"
            addCategory(Intent.CATEGORY_OPENABLE)
            putExtra(Intent.EXTRA_TITLE, title)
        }, request)
    }

    @Deprecated("Activity result API retained without an AndroidX dependency")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK || data?.data == null) return
        val uri = data.data!!
        val image = requestCode == IMAGE_REQUEST
        val bitmap = decodedBitmap
        val log = packetLog
        worker.submit {
            try {
                val output = contentResolver.openOutputStream(uri)
                    ?: throw IOException("Could not open the selected document")
                output.use {
                    if (image) {
                        val value = bitmap ?: return@submit
                        if (!value.compress(Bitmap.CompressFormat.PNG, 100, it))
                            throw IOException("PNG encoding failed")
                    } else it.write((log ?: "").toByteArray(Charsets.UTF_8))
                }
                main.post { statusView.setText(R.string.digital_save_complete) }
            } catch (_: IOException) {
                main.post { statusView.setText(R.string.digital_save_failed) }
            } catch (_: SecurityException) {
                main.post { statusView.setText(R.string.digital_save_failed) }
            }
        }
    }

    override fun onState(code: String) {
        if (shuttingDown) return
        if (code == "radio_host_connecting") {
            statusView.setText(R.string.radio_host_connecting)
        } else if (code == "radio_audio_ready") {
            capture = RadioPcmCapture()
            decodeButton.isEnabled = true
            channelRx.isEnabled = false
            channelTx.isEnabled = false
            refreshTxControls()
            statusView.setText(R.string.radio_audio_stream_active)
        } else if (code == "radio_audio_transport_ready") {
            statusView.setText(R.string.radio_host_transport_ready)
        } else statusView.text = getString(R.string.radio_state, code)
    }

    override fun onStatus(status: RadioHostStatus) {
        currentStatus = status
        statusReceivedAt = SystemClock.elapsedRealtime()
        if (status.operationProfile != "STANDALONE_MANUAL") manualProfileConfirmed = false
        radioChannels = status.availableChannels.sorted()
        val labels = if (radioChannels.isEmpty()) listOf(getString(R.string.radio_no_channels))
            else radioChannels
        val oldRx = channelRx.selectedItem?.toString()
        val oldTx = channelTx.selectedItem?.toString()
        channelRx.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, labels)
        channelTx.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, labels)
        channelRx.setSelection(radioChannels.indexOf(status.rxChannel).takeIf { it >= 0 } ?: 0)
        val preferredTx = radioChannels.indexOf(status.txChannel).takeIf { it >= 0 }
            ?: radioChannels.indexOfFirst { it != status.rxChannel }.takeIf { it >= 0 } ?: 0
        channelTx.setSelection(preferredTx)
        if (oldRx != null && radioChannels.contains(oldRx)) channelRx.setSelection(radioChannels.indexOf(oldRx))
        if (oldTx != null && radioChannels.contains(oldTx)) channelTx.setSelection(radioChannels.indexOf(oldTx))
        rxHz.setText(String.format(Locale.ROOT, "%d", status.rxHz))
        txHz.setText(String.format(Locale.ROOT, "%d", status.txHz))
        val modeIndex = listOf("FM", "AM", "USB").indexOf(status.mode)
        if (modeIndex >= 0) mode.setSelection(modeIndex)
        profileButton.isEnabled = status.operationProfile == "STANDALONE_MANUAL"
        polarizationButton.isEnabled = status.polarizationCapabilities.isNotEmpty()
        decodeButton.isEnabled = transport.readyForAudio && capture != null
        monitorButton.isEnabled = transport.readyForAudio
        refreshTxControls()
        val summary = getString(R.string.radio_status_summary,
            status.operationProfile, status.rxChannel, status.txChannel, status.mode,
            status.rxHz, status.txHz, if (status.sdrReady) getString(R.string.yes) else getString(R.string.no),
            if (status.physicalArm) getString(R.string.yes) else getString(R.string.no),
            if (status.physicalPtt) getString(R.string.yes) else getString(R.string.no),
            status.fault ?: getString(R.string.no))
        val profileSummary = status.profiles.toSortedMap().entries.joinToString("\n") { (channel, profile) ->
            getString(R.string.radio_profile_summary, channel, profile.serial, profile.rxHzReadback,
                profile.txHzReadback, profile.rxRateReadback, profile.txRateReadback,
                profile.rxReads, profile.queueDepth, profile.fault ?: getString(R.string.no))
        }
        statusView.text = if (profileSummary.isEmpty()) summary
            else "$summary\n$profileSummary"
    }

    override fun onAudioReady(rxChannel: String, txChannel: String, mtu: Int) {
        decodeButton.isEnabled = false
        refreshTxControls()
        monitorButton.isEnabled = true
        statusView.text = getString(R.string.radio_transport_ready, rxChannel, txChannel, mtu)
    }

    override fun onAudioBlock(block: PcmBlock, channel: String) {
        try {
            val current = capture ?: return
            if (current.append(block)) {
                stopVoiceMonitor()
                statusView.setText(R.string.radio_receive_limit_reached)
                transport.stopAudio {
                    channelRx.isEnabled = true
                    channelTx.isEnabled = true
                    if (current.failed) statusView.setText(R.string.radio_capture_invalid)
                    else decodeCapture(current)
                }
                return
            }
            decodeButton.isEnabled = true
            if (monitoringVoice && !playbackQueue.offer(block.samples.clone())) {
                onAudioCaptureFailure("radio_voice_playback_queue_full")
                return
            }
        } catch (failure: ProtocolFailure) {
            onAudioCaptureFailure(failure.code)
            return
        }
    }

    override fun onHostEvent(path: String, data: org.json.JSONObject) {
        if (path == "/fault") {
            stopTransmit("radio_host_fault")
            capture?.failed = true
            stopVoiceMonitor()
            decodeButton.isEnabled = false
        }
    }

    override fun onFailure(code: String) {
        stopTransmit(code)
        stopVoiceMonitor()
        statusView.text = getString(R.string.radio_host_failed, code)
        capture?.failed = true
        decodeButton.isEnabled = false
    }

    override fun onDisconnected() {
        stopTransmit(null)
        currentStatus = null
        statusReceivedAt = 0
        manualProfileConfirmed = false
        capture = null
        stopVoiceMonitor()
        decodeButton.isEnabled = false
        voiceButton.isEnabled = false
        transmitMessageButton.isEnabled = false
        profileButton.isEnabled = false
        polarizationButton.isEnabled = false
        orbitOverview.submitHostRouteResult("/rotor/status", null, "radio_host_not_authenticated")
        statusView.setText(R.string.radio_disconnected)
    }

    private fun safeShutdown(finishActivity: Boolean = false) {
        if (shuttingDown) {
            if (finishActivity) finish()
            return
        }
        shuttingDown = true
        txCancelled = true
        if (finishActivity) main.removeCallbacks(txControlsRefresh)
        main.removeCallbacks(leaseRenewal)
        main.removeCallbacks(txStatusRefresh)
        main.removeCallbacks(txTimeout)
        refreshTxControls()
        txTask?.cancel(true)
        val recorder = activeRecorder
        try { if (recorder?.recordingState == AudioRecord.RECORDSTATE_RECORDING) recorder.stop() }
        catch (_: IllegalStateException) { }
        capture = null
        stopVoiceMonitor()
        if (::stopTransmitButton.isInitialized) stopTransmitButton.isEnabled = false
        if (transport.readyForAudio) {
            transport.setPtt(false) {
                transport.stopAudio {
                    transport.disconnect()
                    if (finishActivity) finish()
                }
            }
            main.postDelayed({
                transport.disconnect()
                if (finishActivity) finish()
            }, SHUTDOWN_TIMEOUT_MS)
        } else {
            transport.disconnect()
            if (finishActivity) finish()
        }
    }

    override fun onStop() {
        main.removeCallbacks(txControlsRefresh)
        safeShutdown()
        super.onStop()
    }

    override fun onDestroy() {
        safeShutdown()
        worker.shutdownNow()
        super.onDestroy()
    }

    private class RadioPcmCapture {
        private val samples = ShortArray(SAMPLE_RATE * AudioPcm.MAX_CAPTURE_SECONDS)
        private var size = 0
        private var nextSequence: Long? = null
        private var nextSampleIndex: Long? = null
        @Volatile var failed = false

        @Synchronized fun append(block: PcmBlock): Boolean {
            if (failed) throw ProtocolFailure("radio_capture_invalid")
            if (block.samples.isEmpty())
                throw ProtocolFailure("audio_duration_limit")
            if ((nextSequence != null && block.sequence != nextSequence) ||
                (nextSampleIndex != null && block.firstSampleCounter != nextSampleIndex))
                throw ProtocolFailure("radio_audio_discontinuity")
            if (block.samples.size > samples.size - size) return true
            block.samples.copyInto(samples, size)
            size += block.samples.size
            nextSequence = (block.sequence + 1) and 0xffffffffL
            nextSampleIndex = (block.firstSampleCounter + block.samples.size) and 0xffffffffL
            return size == samples.size
        }

        @Synchronized fun snapshot(): ShortArray {
            if (failed) throw ProtocolFailure("radio_capture_invalid")
            return samples.copyOf(size)
        }
    }

    companion object {
        private const val SAMPLE_RATE = RadioHostWire.AUDIO_RATE
        private const val LEASE_RENEWAL_MS = 150L
        private const val TX_STATUS_REFRESH_MS = 1000L
        private const val MAX_TX_DURATION_MS = 240_000L
        private const val STATUS_MAX_AGE_MS = 2000L
        private const val TX_CONTROLS_REFRESH_MS = 250L
        private const val SHUTDOWN_TIMEOUT_MS = 800L
        private const val REQUEST_BLUETOOTH = 51
        private const val REQUEST_MICROPHONE = 52
        private const val IMAGE_REQUEST = 53
        private const val LOG_REQUEST = 54
        private const val APRS_PREFS = "aprs_local_station"
    }
}
