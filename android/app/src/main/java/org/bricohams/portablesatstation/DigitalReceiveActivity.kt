package org.bricohams.portablesatstation

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.media.AudioDeviceInfo
import android.media.AudioFormat
import android.media.AudioManager
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.Spinner
import android.widget.TextView
import android.text.Editable
import android.text.TextWatcher
import java.io.IOException
import java.util.concurrent.CancellationException
import java.util.concurrent.Executors
import java.util.concurrent.Future

class DigitalReceiveActivity : Activity() {
    private data class AudioInput(val device: AudioDeviceInfo, val label: String)
    private enum class DigitalMode { PD120, PD180, AX25_APRS }

    private val main = Handler(Looper.getMainLooper())
    private val worker = Executors.newSingleThreadExecutor()
    private lateinit var modePicker: Spinner
    private lateinit var inputPicker: Spinner
    private lateinit var status: TextView
    private lateinit var imageView: ImageView
    private lateinit var startButton: Button
    private lateinit var importButton: Button
    private lateinit var stopButton: Button
    private lateinit var saveButton: Button
    private lateinit var saveLogButton: Button
    private lateinit var stationCall: EditText
    private lateinit var messageRecipient: EditText
    private lateinit var messageBody: EditText
    private lateinit var messageId: EditText
    private lateinit var digipeaterPath: EditText
    private lateinit var plaintextConfirmation: CheckBox
    private lateinit var exportTxButton: Button
    private lateinit var inboxView: TextView
    private var inputs = emptyList<AudioInput>()
    @Volatile private var captureRequested = false
    @Volatile private var decodeWhenStopped = false
    @Volatile private var activeRecorder: AudioRecord? = null
    private var captureTask: Future<*>? = null
    private var audioWorkerTask: Future<*>? = null
    private var decodedBitmap: Bitmap? = null
    private var packetLog: String? = null
    private var preparedTransmitWav: ByteArray? = null
    private var screenActive = false
    private var processing = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        buildScreen()
        stationCall.setText(getSharedPreferences(APRS_PREFS, MODE_PRIVATE).getString("station_call", ""))
        refreshInputs()
    }

    private fun clearDecodedResult() {
        decodedBitmap = null
        packetLog = null
        imageView.setImageDrawable(null)
        saveButton.isEnabled = false
        saveLogButton.isEnabled = false
        inboxView.text = getString(R.string.aprs_inbox_empty)
    }

    private fun buildScreen() {
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(24, 16, 24, 24)
        }
        setContentView(ScrollView(this).apply { addView(layout) })
        addText(layout, getString(R.string.digital_title), 22f)
        addText(layout, getString(R.string.digital_scope), 16f)
        addButton(layout, R.string.digital_back) { finish() }
        addText(layout, getString(R.string.digital_mode_label), 16f)
        modePicker = Spinner(this).apply {
            adapter = ArrayAdapter(
                this@DigitalReceiveActivity,
                android.R.layout.simple_spinner_dropdown_item,
                resources.getStringArray(R.array.digital_modes)
            )
        }
        layout.addView(modePicker)
        addText(layout, getString(R.string.audio_input_label), 16f)
        inputPicker = Spinner(this)
        layout.addView(inputPicker)
        addButton(layout, R.string.audio_refresh_inputs) { refreshInputs() }
        addText(layout, getString(R.string.audio_input_warning), 14f)
        startButton = addButton(layout, R.string.audio_start) { requestAudioPermission() }
        stopButton = addButton(layout, R.string.audio_stop_decode) { stopCapture(true) }
        stopButton.isEnabled = false
        importButton = addButton(layout, R.string.audio_import_wav) { openWav() }
        status = addText(layout, getString(R.string.digital_ready), 16f).apply {
            accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_POLITE
        }
        imageView = ImageView(this).apply {
            adjustViewBounds = true
            scaleType = ImageView.ScaleType.FIT_CENTER
            contentDescription = getString(R.string.sstv_image_description)
        }
        layout.addView(
            imageView,
            LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT)
        )
        saveButton = addButton(layout, R.string.sstv_save_image) { saveImage() }
        saveButton.isEnabled = false
        saveLogButton = addButton(layout, R.string.ax25_save_log) { savePacketLog() }
        saveLogButton.isEnabled = false
        addText(layout, getString(R.string.aprs_message_section), 20f)
        addText(layout, getString(R.string.aprs_transport_disclosure), 14f)
        stationCall = addInput(layout, R.string.aprs_station_call)
        messageRecipient = addInput(layout, R.string.aprs_recipient)
        messageBody = addInput(layout, R.string.aprs_message_body)
        messageId = addInput(layout, R.string.aprs_message_id)
        digipeaterPath = addInput(layout, R.string.aprs_digipeater_path)
        plaintextConfirmation = CheckBox(this).apply {
            setText(R.string.aprs_plaintext_confirmation)
            isChecked = false
            layout.addView(this)
        }
        addButton(layout, R.string.aprs_prepare_message) { prepareAprsMessage() }
        exportTxButton = addButton(layout, R.string.aprs_export_audio) { exportTransmitAudio() }
        exportTxButton.isEnabled = false
        listOf(stationCall, messageRecipient, messageBody, messageId, digipeaterPath).forEach { field ->
            field.addTextChangedListener(object : TextWatcher {
                override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
                override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) = Unit
                override fun afterTextChanged(s: Editable?) {
                    if (preparedTransmitWav != null)
                        status.setText(R.string.aprs_prepared_invalidated)
                    preparedTransmitWav = null
                    exportTxButton.isEnabled = false
                    plaintextConfirmation.isChecked = false
                }
            })
        }
        addButton(layout, R.string.aprs_direct_send_unavailable) { status.setText(R.string.aprs_rf_unavailable) }
            .isEnabled = false
        addText(layout, getString(R.string.aprs_inbox_title), 18f)
        inboxView = addText(layout, getString(R.string.aprs_inbox_empty), 14f)
    }

    private fun addText(parent: LinearLayout, value: String, size: Float): TextView =
        TextView(this).apply {
            text = value
            textSize = size
            setPadding(0, 8, 0, 8)
            parent.addView(this)
        }

    private fun addButton(parent: LinearLayout, label: Int, action: () -> Unit): Button =
        Button(this).apply {
            setText(label)
            setOnClickListener { action() }
            parent.addView(this)
        }

    private fun refreshInputs() {
        val manager = getSystemService(Context.AUDIO_SERVICE) as AudioManager
        inputs = manager.getDevices(AudioManager.GET_DEVICES_INPUTS)
            .filter { it.type != AudioDeviceInfo.TYPE_TELEPHONY }
            .map { device -> AudioInput(device, deviceLabel(device)) }
            .sortedWith(compareBy<AudioInput> { !it.isUsb() }.thenBy { it.label.lowercase() })
        inputPicker.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            inputs.map { it.label }
        )
        val preferred = inputs.indexOfFirst { it.isUsb() }
        inputPicker.setSelection(if (preferred >= 0) preferred else inputs.indexOfFirst {
            it.device.type == AudioDeviceInfo.TYPE_BUILTIN_MIC
        }.coerceAtLeast(0))
        status.setText(if (inputs.isEmpty()) R.string.audio_no_input else R.string.digital_ready)
    }

    private fun deviceLabel(device: AudioDeviceInfo): String {
        val kind = when (device.type) {
            AudioDeviceInfo.TYPE_BUILTIN_MIC -> getString(R.string.audio_builtin_mic)
            AudioDeviceInfo.TYPE_USB_DEVICE, AudioDeviceInfo.TYPE_USB_HEADSET ->
                getString(R.string.audio_usb_input)
            AudioDeviceInfo.TYPE_BLUETOOTH_SCO, AudioDeviceInfo.TYPE_BLE_HEADSET ->
                getString(R.string.audio_bluetooth_input)
            else -> getString(R.string.audio_other_input)
        }
        val name = device.productName.toString().trim().take(80)
        return if (name.isEmpty()) "$kind · ${device.id}" else "$kind · $name · ${device.id}"
    }

    private fun AudioInput.isUsb(): Boolean =
        device.type == AudioDeviceInfo.TYPE_USB_DEVICE || device.type == AudioDeviceInfo.TYPE_USB_HEADSET

    private fun requestAudioPermission() {
        if (captureRequested) return
        val selected = inputs.getOrNull(inputPicker.selectedItemPosition)
        if (selected == null) {
            status.setText(R.string.audio_no_input)
            return
        }
        AlertDialog.Builder(this)
            .setMessage(R.string.audio_permission_explanation)
            .setPositiveButton(R.string.confirm) { _, _ ->
                if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED)
                    startCapture(selected)
                else requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), REQUEST_AUDIO)
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode != REQUEST_AUDIO) return
        if (grantResults.firstOrNull() == PackageManager.PERMISSION_GRANTED)
            inputs.getOrNull(inputPicker.selectedItemPosition)?.let { startCapture(it) }
                ?: status.setText(R.string.audio_no_input)
        else status.setText(R.string.audio_permission_denied)
    }

    private fun startCapture(input: AudioInput) {
        if (captureRequested || processing) return
        val selectedMode = selectedMode()
        val ownCallsign = stationCall.text.toString()
        captureRequested = true
        decodeWhenStopped = false
        clearDecodedResult()
        startButton.isEnabled = false
        importButton.isEnabled = false
        stopButton.isEnabled = true
        modePicker.isEnabled = false
        inputPicker.isEnabled = false
        status.setText(R.string.audio_listening)
        captureTask = worker.submit {
            var recorder: AudioRecord? = null
            var count = 0L
            var timedOut = false
            try {
                if (!captureRequested) return@submit
                val current = buildRecorder(input)
                recorder = current
                activeRecorder = current
                current.startRecording()
                val routeDeadline = android.os.SystemClock.elapsedRealtime() + 2000
                var routed = current.routedDevice
                while (captureRequested && (routed == null || routed.id != input.device.id) &&
                    android.os.SystemClock.elapsedRealtime() < routeDeadline) {
                    try {
                        Thread.sleep(50)
                    } catch (_: InterruptedException) {
                        Thread.currentThread().interrupt()
                        break
                    }
                    routed = current.routedDevice
                }
                if (captureRequested && (routed == null || routed.id != input.device.id))
                    throw ProtocolFailure("audio_route_changed")
                if (!captureRequested) return@submit
                val sampleRate = current.sampleRate
                val maxSamples = sampleRate * AudioPcm.MAX_CAPTURE_SECONDS
                val deadline = android.os.SystemClock.elapsedRealtime() +
                    AudioPcm.MAX_CAPTURE_SECONDS * 1000L
                val buffer = BoundedPcmBuffer(sampleRate, maxSamples)
                val source = AudioRecordPcmSource(current, sampleRate) {
                    captureRequested && android.os.SystemClock.elapsedRealtime() < deadline
                }
                count = source.copyTo(buffer, maxSamples)
                timedOut = android.os.SystemClock.elapsedRealtime() >= deadline || count == maxSamples.toLong()
                val shouldDecode = decodeWhenStopped || timedOut
                if (count < sampleRate.toLong() / 10) throw ProtocolFailure("audio_capture_too_short")
                if (shouldDecode) {
                    main.post {
                        status.setText(if (timedOut) R.string.audio_timeout_decoding else R.string.audio_decoding)
                    }
                    decodeSamples(
                        buffer.toAudio().samples,
                        sampleRate,
                        selectedMode,
                        ownCallsign
                    )
                } else {
                    main.post { status.setText(R.string.audio_capture_discarded) }
                }
            } catch (error: ProtocolFailure) {
                main.post { showFailure(error.code) }
            } catch (_: SecurityException) {
                main.post { status.setText(R.string.audio_permission_denied) }
            } catch (_: IllegalStateException) {
                main.post { status.setText(R.string.audio_input_failed) }
            } finally {
                captureRequested = false
                activeRecorder = null
                recorder?.release()
                main.post {
                    startButton.isEnabled = true
                    importButton.isEnabled = true
                    stopButton.isEnabled = false
                    modePicker.isEnabled = true
                    inputPicker.isEnabled = true
                }
            }
        }
    }

    private class AudioRecordPcmSource(
        private val recorder: AudioRecord,
        override val sampleRate: Int,
        private val isActive: () -> Boolean
    ) : PcmSource {
        private var sequence = 0L
        private var sampleCounter = 0L

        override fun readBlock(maxSamples: Int): PcmBlock? {
            if (!isActive()) return null
            val samples = ShortArray(maxSamples)
            val count = recorder.read(samples, 0, maxSamples, AudioRecord.READ_BLOCKING)
            if (count <= 0) {
                if (!isActive()) return null
                throw ProtocolFailure("audio_read_failed")
            }
            val block = PcmBlock(sequence++, sampleCounter, samples.copyOf(count))
            sampleCounter += count
            return block
        }
    }

    private fun buildRecorder(input: AudioInput): AudioRecord {
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED)
            throw ProtocolFailure("audio_permission_denied")
        val rates = listOf(48000, 44100, 22050, 16000, 11025, 8000)
        var initializedAtLeastOnce = false
        for (sampleRate in rates) {
            val minimum = AudioRecord.getMinBufferSize(
                sampleRate,
                AudioFormat.CHANNEL_IN_MONO,
                AudioFormat.ENCODING_PCM_16BIT
            )
            if (minimum <= 0) continue
            for (source in listOf(MediaRecorder.AudioSource.UNPROCESSED, MediaRecorder.AudioSource.MIC)) {
                val recorder = try {
                    AudioRecord.Builder()
                        .setAudioSource(source)
                        .setAudioFormat(
                            AudioFormat.Builder()
                                .setSampleRate(sampleRate)
                                .setChannelMask(AudioFormat.CHANNEL_IN_MONO)
                                .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                                .build()
                        )
                        .setBufferSizeInBytes(maxOf(minimum * 2, sampleRate / 2))
                        .build()
                } catch (_: IllegalArgumentException) {
                    continue
                } catch (_: IllegalStateException) {
                    continue
                }
                if (recorder.state != AudioRecord.STATE_INITIALIZED) {
                    recorder.release()
                    continue
                }
                initializedAtLeastOnce = true
                if (!recorder.setPreferredDevice(input.device)) {
                    recorder.release()
                    throw ProtocolFailure("audio_route_unavailable")
                }
                return recorder
            }
        }
        throw ProtocolFailure(if (initializedAtLeastOnce) "audio_route_unavailable" else "audio_input_unavailable")
    }

    private fun stopCapture(decode: Boolean) {
        if (!captureRequested) return
        decodeWhenStopped = decode
        captureRequested = false
        val recorder = activeRecorder
        if (recorder?.recordingState == AudioRecord.RECORDSTATE_RECORDING) {
            try {
                recorder.stop()
            } catch (_: IllegalStateException) {
                if (screenActive) status.setText(R.string.audio_input_failed)
            }
        }
        if (!decode) captureTask?.cancel(true)
    }

    private fun openWav() {
        if (captureRequested || processing) {
            status.setText(R.string.audio_busy)
            return
        }
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            type = "*/*"
            addCategory(Intent.CATEGORY_OPENABLE)
            putExtra(Intent.EXTRA_MIME_TYPES, arrayOf("audio/wav", "audio/x-wav", "audio/wave"))
        }
        startActivityForResult(intent, REQUEST_OPEN_WAV)
    }

    @Deprecated("Activity result API retained to avoid adding an AndroidX dependency")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK) return
        val uri = data?.data ?: return
        when (requestCode) {
            REQUEST_OPEN_WAV -> {
                if (captureRequested || processing) {
                    status.setText(R.string.audio_busy)
                    return
                }
                val selectedMode = selectedMode()
                val ownCallsign = stationCall.text.toString()
                setProcessing(true)
                clearDecodedResult()
                status.setText(R.string.audio_reading_wav)
                audioWorkerTask = worker.submit {
                    try {
                        val stream = contentResolver.openInputStream(uri)
                            ?: throw IOException("Unable to open the selected document")
                        val audio = stream.use { PcmWav.read(it) }
                        decodeSamples(audio.samples, audio.sampleRate, selectedMode, ownCallsign)
                    } catch (error: ProtocolFailure) {
                        main.post { showFailure(error.code) }
                    } catch (_: IOException) {
                        main.post { status.setText(R.string.audio_wav_read_failed) }
                    } catch (_: SecurityException) {
                        main.post { status.setText(R.string.audio_wav_read_failed) }
                    } catch (_: CancellationException) {
                        main.post { status.setText(R.string.audio_cancelled) }
                    } finally {
                        main.post { setProcessing(false) }
                    }
                }
            }
            REQUEST_SAVE_IMAGE -> saveImageTo(uri)
            REQUEST_SAVE_LOG -> saveLogTo(uri)
            REQUEST_SAVE_TX_WAV -> saveTransmitWavTo(uri)
        }
    }

    private fun selectedMode(): DigitalMode = when (modePicker.selectedItemPosition) {
        MODE_PD120 -> DigitalMode.PD120
        MODE_PD180 -> DigitalMode.PD180
        MODE_AX25 -> DigitalMode.AX25_APRS
        else -> throw ProtocolFailure("digital_mode_invalid")
    }

    private fun decodeSamples(
        samples: ShortArray,
        sampleRate: Int,
        selectedMode: DigitalMode,
        ownCallsign: String
    ) {
        try {
            when (selectedMode) {
                DigitalMode.PD120, DigitalMode.PD180 -> {
                    val sstvMode = if (selectedMode == DigitalMode.PD120)
                        SstvModeChoice.PD120 else SstvModeChoice.PD180
                    val image = SstvDecoder.decode(samples, sampleRate, sstvMode) {
                        Thread.currentThread().isInterrupted
                    }
                    val bitmap = Bitmap.createBitmap(
                        image.pixels,
                        image.mode.width,
                        image.mode.height,
                        Bitmap.Config.ARGB_8888
                    )
                    main.post {
                        decodedBitmap = bitmap
                        packetLog = null
                        imageView.setImageBitmap(bitmap)
                        saveButton.isEnabled = true
                        saveLogButton.isEnabled = false
                        status.text = getString(
                            R.string.sstv_decoded,
                            image.mode.name,
                            image.mode.width,
                            image.mode.height,
                            image.verifiedLines
                        )
                    }
                }
                DigitalMode.AX25_APRS -> {
                    val packets = Ax25AfskDecoder.decode(samples, sampleRate) {
                        Thread.currentThread().isInterrupted
                    }
                    val log = packets.joinToString("\n\n") { it.logEntry() }
                    val inbox = AprsInbox.addressedTo(packets, ownCallsign)
                    main.post {
                        decodedBitmap = null
                        packetLog = log
                        imageView.setImageDrawable(null)
                        status.text = getString(R.string.ax25_decoded, packets.size, log)
                        inboxView.text = if (inbox.isEmpty()) getString(R.string.aprs_inbox_empty)
                            else inbox.joinToString("\n\n")
                        saveButton.isEnabled = false
                        saveLogButton.isEnabled = true
                    }
                }
                else -> throw ProtocolFailure("digital_mode_invalid")
            }
        } catch (error: ProtocolFailure) {
            main.post { showFailure(error.code) }
        } catch (_: CancellationException) {
            main.post { status.setText(R.string.audio_cancelled) }
        }
    }

    private fun saveImage() {
        if (decodedBitmap == null) return
        startActivityForResult(
            Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                type = "image/png"
                addCategory(Intent.CATEGORY_OPENABLE)
                putExtra(Intent.EXTRA_TITLE, "PortableSatStation-SSTV.png")
            },
            REQUEST_SAVE_IMAGE
        )
    }

    private fun saveImageTo(uri: android.net.Uri) {
        val bitmap = decodedBitmap ?: return
        setProcessing(true)
        audioWorkerTask = worker.submit {
            try {
                val output = contentResolver.openOutputStream(uri)
                    ?: throw IOException("Unable to open the selected destination")
                output.use {
                    if (!bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
                        throw IOException("PNG encoding failed")
                }
                main.post { status.setText(R.string.sstv_saved) }
            } catch (_: IOException) {
                main.post { status.setText(R.string.digital_save_failed) }
            } catch (_: SecurityException) {
                main.post { status.setText(R.string.digital_save_failed) }
            } finally {
                main.post { setProcessing(false) }
            }
        }
    }

    private fun savePacketLog() {
        if (packetLog == null) return
        startActivityForResult(
            Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                type = "text/plain"
                addCategory(Intent.CATEGORY_OPENABLE)
                putExtra(Intent.EXTRA_TITLE, "PortableSatStation-AX25-APRS.txt")
            },
            REQUEST_SAVE_LOG
        )
    }

    private fun saveLogTo(uri: android.net.Uri) {
        val log = packetLog ?: return
        setProcessing(true)
        audioWorkerTask = worker.submit {
            try {
                val output = contentResolver.openOutputStream(uri)
                    ?: throw IOException("Unable to open the selected destination")
                output.use { it.write(log.toByteArray(Charsets.UTF_8)) }
                main.post { status.setText(R.string.ax25_log_saved) }
            } catch (_: IOException) {
                main.post { status.setText(R.string.digital_save_failed) }
            } catch (_: SecurityException) {
                main.post { status.setText(R.string.digital_save_failed) }
            } finally {
                main.post { setProcessing(false) }
            }
        }
    }

    private fun addInput(parent: LinearLayout, hint: Int): EditText =
        EditText(this).apply {
            setHint(hint)
            setSingleLine(true)
            parent.addView(this)
        }

    private fun prepareAprsMessage() {
        try {
            if (!plaintextConfirmation.isChecked)
                throw ProtocolFailure("aprs_plaintext_not_confirmed")
            val source = AprsAddressing.normalizeCallsign(stationCall.text.toString())
                ?: throw ProtocolFailure("aprs_source_invalid")
            val destination = AprsAddressing.normalizeStation(messageRecipient.text.toString())
                ?: throw ProtocolFailure("aprs_destination_invalid")
            val path = AprsAddressing.parsePath(digipeaterPath.text.toString())
                ?: throw ProtocolFailure("aprs_path_invalid")
            val id = messageId.text.toString().trim().ifEmpty { null }
            val information = AprsMessageCodec.encodeMessageInformation(
                destination, messageBody.text.toString(), id
            )
            val frame = AprsMessageCodec.encodeUiFrame(source, "APRS", path, information)
            val wav = Bell202Encoder.encode(frame).toWav()
            getSharedPreferences(APRS_PREFS, MODE_PRIVATE).edit().putString("station_call", source).apply()
            preparedTransmitWav = wav
            exportTxButton.isEnabled = true
            status.setText(R.string.aprs_message_prepared)
        } catch (error: ProtocolFailure) {
            preparedTransmitWav = null
            exportTxButton.isEnabled = false
            status.text = when (error.code) {
                "aprs_source_invalid" -> getString(R.string.aprs_invalid_station)
                "aprs_destination_invalid" -> getString(R.string.aprs_invalid_recipient)
                "aprs_path_invalid" -> getString(R.string.aprs_invalid_path)
                "aprs_message_id_invalid" -> getString(R.string.aprs_invalid_message_id)
                "aprs_plaintext_not_confirmed" -> getString(R.string.aprs_plaintext_required)
                else -> getString(R.string.aprs_invalid_message)
            }
        }
    }

    private fun exportTransmitAudio() {
        if (preparedTransmitWav == null) {
            status.setText(R.string.aprs_nothing_prepared)
            return
        }
        startActivityForResult(
            Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                type = "audio/wav"
                addCategory(Intent.CATEGORY_OPENABLE)
                putExtra(Intent.EXTRA_TITLE, "PortableSatStation-APRS-message.wav")
            },
            REQUEST_SAVE_TX_WAV
        )
    }

    private fun saveTransmitWavTo(uri: android.net.Uri) {
        val wav = preparedTransmitWav ?: return
        setProcessing(true)
        audioWorkerTask = worker.submit {
            try {
                val output = contentResolver.openOutputStream(uri)
                    ?: throw IOException("Unable to open the selected destination")
                output.use { it.write(wav) }
                main.post { status.setText(R.string.aprs_audio_exported_not_sent) }
            } catch (_: IOException) {
                main.post { status.setText(R.string.digital_save_failed) }
            } catch (_: SecurityException) {
                main.post { status.setText(R.string.digital_save_failed) }
            } finally {
                main.post { setProcessing(false) }
            }
        }
    }

    private fun setProcessing(value: Boolean) {
        processing = value
        startButton.isEnabled = !value && !captureRequested
        importButton.isEnabled = !value && !captureRequested
        modePicker.isEnabled = !value && !captureRequested
        inputPicker.isEnabled = !value && !captureRequested
        saveButton.isEnabled = !value && decodedBitmap != null
        saveLogButton.isEnabled = !value && packetLog != null
        exportTxButton.isEnabled = !value && preparedTransmitWav != null
    }

    private fun showFailure(code: String) {
        status.text = when (code) {
            "audio_route_changed", "audio_route_unavailable" ->
                getString(R.string.audio_route_failed)
            "audio_permission_denied" -> getString(R.string.audio_permission_denied)
            "audio_read_failed", "audio_input_unavailable" -> getString(R.string.audio_input_failed)
            "aprs_source_invalid" -> getString(R.string.aprs_invalid_station)
            "aprs_destination_invalid" -> getString(R.string.aprs_invalid_recipient)
            "aprs_path_invalid" -> getString(R.string.aprs_invalid_path)
            "aprs_message_invalid" -> getString(R.string.aprs_invalid_message)
            "aprs_message_id_invalid" -> getString(R.string.aprs_invalid_message_id)
            "audio_capture_too_short", "audio_too_short" -> getString(R.string.audio_too_short)
            "audio_sample_rate", "audio_duration_limit" -> getString(R.string.audio_limit_failed)
            "wav_riff", "wav_wave", "wav_format", "wav_pcm_format", "wav_data",
            "wav_data_missing", "wav_format_missing", "wav_chunk_size", "wav_size", "wav_truncated" ->
                getString(R.string.audio_wav_invalid, code)
            else -> getString(R.string.digital_decode_failed, code)
        }
        saveButton.isEnabled = false
        saveLogButton.isEnabled = false
    }

    override fun onStart() {
        super.onStart()
        screenActive = true
    }

    override fun onStop() {
        screenActive = false
        stopCapture(false)
        captureTask?.cancel(true)
        audioWorkerTask?.cancel(true)
        super.onStop()
    }

    override fun onDestroy() {
        stopCapture(false)
        captureTask?.cancel(true)
        audioWorkerTask?.cancel(true)
        worker.shutdownNow()
        super.onDestroy()
    }

    companion object {
        private const val REQUEST_AUDIO = 31
        private const val REQUEST_OPEN_WAV = 32
        private const val REQUEST_SAVE_IMAGE = 33
        private const val REQUEST_SAVE_LOG = 34
        private const val REQUEST_SAVE_TX_WAV = 35
        private const val MODE_PD120 = 0
        private const val MODE_PD180 = 1
        private const val MODE_AX25 = 2
        private const val APRS_PREFS = "aprs_local_station"
    }
}
