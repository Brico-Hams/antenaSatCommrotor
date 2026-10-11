package org.bricohams.portablesatstation

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanFilter
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.ParcelUuid
import android.text.InputType
import android.view.View
import android.widget.*
import org.json.JSONObject
import org.bricohams.portablesatstation.orbit.SatelliteOverviewView
import java.io.IOException
import java.security.GeneralSecurityException
import java.util.concurrent.Executors
import java.util.concurrent.Future

class MainActivity : Activity() {
    private val main = Handler(Looper.getMainLooper())
    private lateinit var layout: LinearLayout
    private lateinit var devices: LinearLayout
    private lateinit var message: TextView
    private lateinit var statusView: TextView
    private lateinit var guide: TextView
    private lateinit var token: EditText
    private lateinit var satellitePicker: Spinner
    private lateinit var passView: TextView
    private var orbitOverview: SatelliteOverviewView? = null
    private var satelliteIds = emptyList<Int>()
    private var satelliteItems = emptyList<SatelliteData>()
    private var catalogOffset = 0
    private var nextCatalogOffset = -1
    private lateinit var transport: BleTransport
    private lateinit var vault: TokenVault
    private val controls = mutableListOf<Button>()
    private var scanActive = false
    private val found = mutableSetOf<String>()
    private var selected: BluetoothDevice? = null
    private var selectedToken: String? = null
    private var latestStatus: RotorStatus? = null
    private val downloads = Executors.newSingleThreadExecutor()
    private var downloadTask: Future<*>? = null
    @Volatile private var downloadGeneration = 0
    @Volatile private var downloadCancelled = false
    private lateinit var cache: TleCache
    private var cachedCatalogue: TleCatalogue? = null
    private lateinit var providerPicker: Spinner
    private lateinit var localSatellitePicker: Spinner
    private lateinit var downloadButton: Button
    private lateinit var localTleInfo: TextView
    private var transfer: TleTransfer? = null
    private var pendingTransfer: TleCatalogue? = null
    private var stopAfterTransfer = false
    private val transferTimeout = Runnable {
        pendingTransfer = null; transfer = null; stopAfterTransfer = false
        transport.disconnect(); failure("tle_transfer_timeout")
    }
    private var passQueries = 0
    private var passJobActive = false
    private val passQuery = Runnable {
        if (passJobActive && transport.ready && transfer == null && pendingTransfer == null) {
            if (!transport.busy && passQueries < 60) {
                passQueries++
                transport.command("passes", JSONObject())
            } else {
                passJobActive = false; failure("pass_query_limit")
            }
        }
    }
    private var phase = CalibrationPhase.CHECK_AND_HOME
    private val scanEnd = Runnable { stopScan(); message.setText(R.string.scan_complete) }
    private val bondTimeout = Runnable { selected = null; selectedToken = null; failure("pair_timeout") }
    private val preferences by lazy { getSharedPreferences("physical-guide", MODE_PRIVATE) }
    private val poll = object : Runnable {
        override fun run() {
            if (transport.ready && !transport.busy && transfer == null && pendingTransfer == null && !passJobActive)
                transport.command("status", JSONObject())
            main.postDelayed(this, 2000)
        }
    }
    private val bondReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            try {
                @Suppress("DEPRECATION")
                val device = intent.getParcelableExtra<BluetoothDevice>(BluetoothDevice.EXTRA_DEVICE) ?: return
                if (device.address != selected?.address) return
                when (intent.getIntExtra(BluetoothDevice.EXTRA_BOND_STATE, BluetoothDevice.BOND_NONE)) {
                    BluetoothDevice.BOND_BONDED -> {
                        main.removeCallbacks(bondTimeout)
                        val credential = selectedToken ?: return
                        selectedToken = null
                        transport.connect(device, credential)
                    }
                    BluetoothDevice.BOND_NONE -> {
                        main.removeCallbacks(bondTimeout)
                        selected = null
                        selectedToken = null
                        transport.disconnect()
                        failure("pair_failed")
                    }
                }
            } catch (_: SecurityException) { cancelBond(); failure("permission_denied") }
        }
    }
    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            main.post {
                if (!scanActive) return@post
                try {
                    val device = result.device
                    if (!found.add(device.address)) return@post
                    val name = device.name ?: "PortableSatStation"
                    button(getString(R.string.select_device, name, device.address), devices) {
                        choose(device)
                    }
                } catch (_: SecurityException) { failure("permission_denied"); stopScan() }
            }
        }
        override fun onScanFailed(errorCode: Int) {
            main.post { stopScan(); failure("scan_failed_$errorCode") }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(android.view.WindowManager.LayoutParams.FLAG_SECURE)
        vault = TokenVault(this)
        cache = TleCache(this)
        transport = BleTransport(this, object : BleTransport.Listener {
            override fun onStatus(status: RotorStatus) {
                latestStatus = status
                val yes = getString(R.string.yes)
                val no = getString(R.string.no)
                statusView.text = getString(R.string.status_summary, status.mode, status.fault,
                    status.az, status.el, if (status.homed) yes else no, if (status.calibrated) yes else no,
                    if (status.utcValid) java.time.Instant.ofEpochSecond(status.utc).toString() else no,
                    if (status.siteValid) getString(R.string.site_coordinates, status.latitude,
                        status.longitude, status.altitude) else no)
                controls.forEach { it.isEnabled = transport.ready }
                if (transport.ready) message.setText(R.string.connected)
                pendingTransfer?.let { value ->
                    pendingTransfer = null
                    try {
                        val upload = TleTransfer(value)
                        val command = upload.begin(status)
                        transfer = upload
                        main.postDelayed(transferTimeout, TRANSFER_STALL_MS)
                        transport.command(command.operation, command.body)
                        localTleInfo.text = getString(R.string.transfer_progress, 0, upload.size)
                    } catch (error: ProtocolFailure) { failure(error.code) }
                }
            }
            override fun onResponse(operation: String, body: JSONObject) {
                if (operation.startsWith("tle/")) {
                    val upload = transfer ?: throw ProtocolFailure("tle_transfer_sequence")
                    val next = upload.acknowledge(operation, body)
                    // Stall detection: every acknowledged step proves the link is alive, so a
                    // large catalogue over 20-byte BLE frames is not cut off by a fixed total time.
                    if (next != null) { main.removeCallbacks(transferTimeout); main.postDelayed(transferTimeout, TRANSFER_STALL_MS) }
                    localTleInfo.text = getString(R.string.transfer_progress, upload.received, upload.size)
                    if (next != null) transport.command(next.operation, next.body)
                    else {
                        main.removeCallbacks(transferTimeout)
                        transfer = null
                        localTleInfo.setText(if (upload.committed) R.string.transfer_complete else R.string.transfer_aborted)
                        satelliteIds = emptyList(); satelliteItems = emptyList(); nextCatalogOffset = -1
                        if (stopAfterTransfer) {
                            stopAfterTransfer = false
                            transport.command("stop", JSONObject(), true)
                        }
                    }
                    return
                }
                if (operation == "home" || operation == "clear") {
                    latestStatus = null
                    setPhase(CalibrationPhase.CHECK_AND_HOME)
                }
                if (operation == "catalog") {
                    val page = CatalogPage.parse(body, catalogOffset)
                    satelliteItems = (if (catalogOffset == 0) emptyList() else satelliteItems) + page.satellites
                    if (satelliteItems.size > 100) throw ProtocolFailure("invalid_catalog")
                    nextCatalogOffset = page.nextOffset
                    satelliteIds = satelliteItems.map { it.id }
                    satellitePicker.adapter = ArrayAdapter(this@MainActivity,
                        android.R.layout.simple_spinner_dropdown_item, satelliteItems.map {
                            getString(R.string.satellite_entry, it.id, it.name)
                        })
                }
                if (operation == "passes") {
                    val result = PassData.parse(body)
                    passView.text = getString(R.string.passes_full,
                        if (result.calculating) getString(R.string.calculating) else "",
                        result.passes.joinToString("\n") {
                            getString(R.string.pass_entry, java.time.Instant.ofEpochSecond(it.aos).toString(),
                                java.time.Instant.ofEpochSecond(it.los).toString(), it.maxEl,
                                java.time.Instant.ofEpochSecond(it.peak).toString(),
                                if (it.partial) getString(R.string.partial_pass) else "")
                        })
                    if (result.calculating && passJobActive && passQueries < 60)
                        main.postDelayed(passQuery, 1500)
                    else {
                        if (result.calculating && passJobActive) failure("pass_query_limit")
                        passJobActive = false
                    }
                }
                message.setText(R.string.ack)
            }
            override fun onFailure(code: String) { failure(code) }
            override fun onDisconnected() {
                latestStatus = null
                main.removeCallbacks(transferTimeout); main.removeCallbacks(passQuery)
                transfer = null; pendingTransfer = null; stopAfterTransfer = false; passJobActive = false
                satelliteIds = emptyList()
                satelliteItems = emptyList(); nextCatalogOffset = -1
                controls.forEach { it.isEnabled = false }
                statusView.setText(R.string.disconnected)
            }
        })
        layout = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(24, 16, 24, 16) }
        setContentView(ScrollView(this).apply { addView(layout) })
        Branding.header(this, layout, Branding.Topic.MAIN)
        text(getString(R.string.app_name))
        text(getString(R.string.disclaimer))
        message = text(getString(R.string.disconnected)).apply { accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_POLITE }
        statusView = text(getString(R.string.disconnected))
        button(R.string.open_digital_receiver) {
            startActivity(Intent(this, DigitalReceiveActivity::class.java))
        }
        button(R.string.radio_host_open) {
            startActivity(Intent(this, RadioHostActivity::class.java))
        }
        orbitOverview = SatelliteOverviewView(this).apply {
            submitSnapshot(null)
            onNotificationPermissionRequested = { requestOrbitNotificationPermission() }
        }
        layout.addView(orbitOverview)
        text(getString(R.string.download_privacy))
        providerPicker = Spinner(this).apply {
            adapter = ArrayAdapter(this@MainActivity, android.R.layout.simple_spinner_dropdown_item,
                TleProvider.entries.map { it.label })
        }
        layout.addView(providerPicker)
        downloadButton = button(R.string.download_tle) {
            val provider = TleProvider.entries[providerPicker.selectedItemPosition]
            loadCatalogue { cancelled, progress -> TleDownload.fetch(provider, cancelled, progress) }
        }
        button(R.string.cancel_download) { cancelDownload() }
        button(R.string.import_tle_file) {
            if (transfer != null || pendingTransfer != null) { message.setText(R.string.busy); return@button }
            startActivityForResult(Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                type = "*/*"; addCategory(Intent.CATEGORY_OPENABLE)
            }, 2)
        }
        localTleInfo = text(getString(R.string.no_cached_tle))
        localSatellitePicker = Spinner(this).also { layout.addView(it) }
        try { cache.load()?.let { showCatalogue(it) } }
        catch (_: IOException) { failure("tle_cache_unavailable") }
        catch (error: ProtocolFailure) { failure(error.code) }
        button(R.string.transfer_catalogue) { cachedCatalogue?.let { requestTransfer(it) } ?: failure("tle_no_cache") }
        button(R.string.transfer_selected) {
            val entry = cachedCatalogue?.entries?.getOrNull(localSatellitePicker.selectedItemPosition)
            if (entry == null) failure("tle_no_cache")
            else requestTransfer(TleCatalogue.parse(entry.text().toByteArray(Charsets.US_ASCII)))
        }
        button(R.string.abort_transfer) { cancelTransfer(false) }
        token = field(R.string.token, password = true)
        token.importantForAutofill = View.IMPORTANT_FOR_AUTOFILL_NO_EXCLUDE_DESCENDANTS
        token.imeOptions = token.imeOptions or android.view.inputmethod.EditorInfo.IME_FLAG_NO_PERSONALIZED_LEARNING
        token.setSaveEnabled(false)
        try { vault.load()?.let { token.setText(it) } }
        catch (_: GeneralSecurityException) { message.setText(R.string.token_error) }
        catch (_: IOException) { message.setText(R.string.token_error) }
        catch (_: IllegalArgumentException) { message.setText(R.string.token_error) }
        button(R.string.save_token) {
            if (token.text.isEmpty()) { message.setText(R.string.token_required); return@button }
            try { vault.save(token.text.toString()); message.setText(R.string.token_saved) }
            catch (_: GeneralSecurityException) { message.setText(R.string.token_error) }
            catch (_: IOException) { message.setText(R.string.token_error) }
            catch (_: IllegalStateException) { message.setText(R.string.token_error) }
        }
        button(R.string.forget_token) {
            stopScan(); cancelBond(); transport.disconnect()
            vault.clear(); token.text.clear()
        }
        button(R.string.scan) { requestScan() }
        devices = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        layout.addView(devices)
        button(R.string.disconnect) { stopScan(); cancelBond(); transport.disconnect() }
        control(R.string.status, "status")
        control(R.string.stop, "stop", priority = true)
        control(R.string.clear, "clear")
        control(R.string.home, "home")
        val az = field(R.string.az).apply { setText("0") }
        val el = field(R.string.el).apply { setText("0") }
        control(R.string.move, "move") {
            JSONObject().put("az", NumericInput.finite(az.text.toString(), -180.0, 180.0))
                .put("el", NumericInput.finite(el.text.toString(), 0.0, 90.0))
        }
        phase = CalibrationPhase.restore(preferences.getString("phase", null))
        guide = text("")
        showGuide()
        button(R.string.next) {
            if (phase == CalibrationPhase.CHECK_AND_HOME && latestStatus?.homed != true) {
                message.setText(R.string.home_required)
            } else setPhase(phase.next())
        }
        button(R.string.restart_wizard) { setPhase(CalibrationPhase.CHECK_AND_HOME) }
        val heading = field(R.string.true_az)
        val level = CheckBox(this).apply { setText(R.string.level) }
        layout.addView(level)
        control(R.string.calibrate, "calibrate") {
            require(level.isChecked) { "level_required" }
            require(latestStatus?.homed == true) { "home_required" }
            JSONObject().put("trueAz", NumericInput.finite(heading.text.toString(), 0.0, 360.0, false))
                .put("levelConfirmed", true)
        }
        // Manual site is rotor configuration; phone location is never read.
        val manual = CheckBox(this).apply { setText(R.string.manual_site) }
        layout.addView(manual)
        val latitude = field(R.string.lat).apply { setText("0") }
        val longitude = field(R.string.lon).apply { setText("0") }
        val altitude = field(R.string.alt).apply { setText("0") }
        control(R.string.site, "site") {
            JSONObject().put("manual", manual.isChecked)
                .put("lat", NumericInput.finite(latitude.text.toString(), -90.0, 90.0))
                .put("lon", NumericInput.finite(longitude.text.toString(), -180.0, 180.0))
                .put("alt", NumericInput.finite(altitude.text.toString(), Protocol.ALT_MIN, Protocol.ALT_MAX))
        }
        text(getString(R.string.satellite_note))
        control(R.string.satellites, "catalog") {
            catalogOffset = 0
            JSONObject().put("offset", 0).put("limit", 10)
        }
        control(R.string.next_catalog, "catalog") {
            require(nextCatalogOffset >= 0) { "no_catalog_page" }
            catalogOffset = nextCatalogOffset
            JSONObject().put("offset", catalogOffset).put("limit", 10)
        }
        satellitePicker = Spinner(this).also { layout.addView(it) }
        control(R.string.select_satellite, "select") {
            val id = satelliteIds.getOrNull(satellitePicker.selectedItemPosition)
                ?: throw IllegalArgumentException("no_satellite")
            JSONObject().put("id", id)
        }
        control(R.string.track, "track") { JSONObject() }
        control(R.string.passes, "passes")
        passView = text("")
        val filter = IntentFilter(BluetoothDevice.ACTION_BOND_STATE_CHANGED)
        if (Build.VERSION.SDK_INT >= 33) registerReceiver(bondReceiver, filter, RECEIVER_EXPORTED)
        else @Suppress("DEPRECATION") registerReceiver(bondReceiver, filter)
    }
    private fun text(value: String): TextView = TextView(this).apply {
        text = value; setPadding(0, 8, 0, 8); this@MainActivity.layout.addView(this)
    }
    private fun field(label: Int, password: Boolean = false): EditText = EditText(this).apply {
        hint = getString(label)
        inputType = if (password) InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            else InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL or InputType.TYPE_NUMBER_FLAG_SIGNED
        this@MainActivity.layout.addView(this)
    }
    private fun button(label: Int, action: () -> Unit): Button = button(getString(label), layout, action)
    private fun button(label: String, parent: LinearLayout, action: () -> Unit): Button = Button(this).apply {
        text = label; setOnClickListener { action() }; parent.addView(this)
    }
    private fun control(label: Int, operation: String, priority: Boolean = false, body: () -> JSONObject = { JSONObject() }) {
        controls += button(label) {
            if (transfer != null || pendingTransfer != null) {
                if (operation == "stop") cancelTransfer(true) else message.setText(R.string.busy)
                return@button
            }
            if (transport.busy && !priority) { message.setText(R.string.busy); return@button }
            try {
                val data = body()
                main.removeCallbacks(passQuery); passJobActive = operation == "passes"
                if (passJobActive) passQueries = 1
                transport.command(operation, data, priority)
            }
            catch (error: IllegalArgumentException) {
                message.setText(when (error.message) {
                    "level_required" -> R.string.level_required
                    "home_required" -> R.string.home_required
                    "no_satellite" -> R.string.no_satellite
                    "no_catalog_page" -> R.string.no_catalog_page
                    else -> R.string.invalid_number
                })
            }
        }.apply { isEnabled = false }
    }
    private fun setPhase(value: CalibrationPhase) {
        phase = value; preferences.edit().putString("phase", phase.name).apply(); showGuide()
    }
    private fun showGuide() {
        val detail = when (phase) {
            CalibrationPhase.CHECK_AND_HOME -> R.string.wizard_1
            CalibrationPhase.LEVEL_AND_ZERO -> R.string.wizard_2
            CalibrationPhase.TRUE_HEADING -> R.string.wizard_3
            CalibrationPhase.CONFIRM -> R.string.wizard_4
        }
        guide.text = getString(R.string.guide_full, getString(R.string.wizard, phase.step), getString(detail))
    }
    private fun failure(code: String) {
        // Only bounded machine codes, never remote JSON, credentials or exception messages.
        val explanation = when (code) {
            "authentication_failed" -> getString(R.string.authentication_failed)
            "protocol_mismatch", "api_version_mismatch", "firmware_version_mismatch" -> getString(R.string.protocol_mismatch)
            "rotor_state_or_control_owner_conflict" -> getString(R.string.control_conflict)
            "ble_request_timeout" -> getString(R.string.timeout)
            "tle_rotor_not_ready_or_fresh" -> getString(R.string.tle_rotor_not_ready)
            "tle_no_cache" -> getString(R.string.no_cached_tle)
            "tle_network", "tle_cache_unavailable" -> getString(R.string.download_failed)
            "tle_download_timeout" -> getString(R.string.tle_http_timeout)
            "tle_http_403", "tle_http_429" -> getString(R.string.tle_http_rate_limited)
            "tle_http_301", "tle_http_302", "tle_http_303", "tle_http_307", "tle_http_308" -> getString(R.string.tle_http_redirect)
            "tle_http_404", "tle_http_410" -> getString(R.string.tle_http_missing)
            "tle_http_500", "tle_http_502", "tle_http_503", "tle_http_504" -> getString(R.string.tle_http_server)
            "pass_query_limit" -> getString(R.string.pass_query_limit)
            "tle_transfer_timeout" -> getString(R.string.tle_transfer_timeout)
            else -> if (code.startsWith("tle_")) getString(R.string.tle_invalid,
                code.take(64).replace(Regex("[^a-zA-Z0-9_ -]"), ""))
            else code.take(64).replace(Regex("[^a-zA-Z0-9_ -]"), "")
        }
        message.text = getString(R.string.failed, explanation)
    }
    private fun requestScan() {
        AlertDialog.Builder(this).setMessage(R.string.permission_rationale)
            .setPositiveButton(R.string.confirm) { _, _ ->
                val permissions = if (Build.VERSION.SDK_INT >= 31)
                    arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
                else arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION)
                if (permissions.all { checkSelfPermission(it) == PackageManager.PERMISSION_GRANTED }) scan()
                else requestPermissions(permissions, 1)
            }.setNegativeButton(R.string.cancel, null).show()
    }
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        when (requestCode) {
            1 -> if (grantResults.isNotEmpty() && grantResults.all { it == PackageManager.PERMISSION_GRANTED }) scan()
                else message.setText(R.string.bluetooth_unavailable)
            ORBIT_NOTIFICATION_PERMISSION -> orbitOverview?.refreshAlertPermission()
        }
    }
    private fun requestOrbitNotificationPermission() {
        if (Build.VERSION.SDK_INT >= 33 &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            AlertDialog.Builder(this).setMessage(R.string.orbit_notification_permission_explanation)
                .setPositiveButton(R.string.confirm) { _, _ ->
                    requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS), ORBIT_NOTIFICATION_PERMISSION)
                }.setNegativeButton(R.string.cancel, null).show()
        } else orbitOverview?.refreshAlertPermission()
    }
    private fun scan() {
        stopScan(); cancelBond(); transport.disconnect()
        devices.removeAllViews(); found.clear()
        try {
            val adapter = getSystemService(BluetoothManager::class.java).adapter
            if (adapter?.isEnabled != true) { message.setText(R.string.bluetooth_unavailable); return }
            val scanner = adapter.bluetoothLeScanner ?: run { message.setText(R.string.bluetooth_unavailable); return }
            scanActive = true
            scanner.startScan(listOf(ScanFilter.Builder().setServiceUuid(ParcelUuid(Protocol.SERVICE)).build()),
                ScanSettings.Builder().setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY).build(), scanCallback)
            main.postDelayed(scanEnd, 15000)
        } catch (_: SecurityException) { scanActive = false; message.setText(R.string.bluetooth_unavailable) }
    }
    private fun stopScan() {
        main.removeCallbacks(scanEnd)
        if (!scanActive) return
        scanActive = false
        try { getSystemService(BluetoothManager::class.java).adapter?.bluetoothLeScanner?.stopScan(scanCallback) }
        catch (_: SecurityException) { message.setText(R.string.bluetooth_unavailable) }
    }
    private fun choose(device: BluetoothDevice) {
        if (token.text.isEmpty()) { message.setText(R.string.token_required); return }
        AlertDialog.Builder(this).setTitle(R.string.pair_title).setMessage(R.string.pair_explanation)
            .setPositiveButton(R.string.confirm) { _, _ ->
                stopScan(); cancelBond(); transport.disconnect()
                try {
                    selected = device
                    val credential = token.text.toString()
                    if (device.bondState == BluetoothDevice.BOND_BONDED) transport.connect(device, credential)
                    else {
                        selectedToken = credential
                        if (!device.createBond()) { cancelBond(); failure("pair_failed") }
                        else main.postDelayed(bondTimeout, 60000)
                    }
                } catch (_: SecurityException) { cancelBond(); failure("permission_denied") }
            }.setNegativeButton(R.string.cancel, null).show()
    }
    private fun cancelBond() { main.removeCallbacks(bondTimeout); selected = null; selectedToken = null }
    private fun showCatalogue(value: TleCatalogue) {
        cachedCatalogue = value
        localSatellitePicker.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item,
            value.entries.map { getString(R.string.local_tle_entry, it.id, it.name,
                java.time.Instant.ofEpochSecond(it.epoch).toString()) })
        localTleInfo.text = getString(R.string.cached_tle, value.entries.size, value.bytes.size, value.sha256)
    }
    private fun showDownloadProgress(generation: Int, bytes: Int, total: Int) {
        main.post {
            if (!downloadCancelled && generation == downloadGeneration)
                localTleInfo.text = getString(R.string.download_progress, bytes, total)
        }
    }
    private fun loadCatalogue(work: (() -> Boolean, (Int, Int) -> Unit) -> TleCatalogue) {
        if (transfer != null || pendingTransfer != null) { message.setText(R.string.busy); return }
        cancelDownload()
        downloadCancelled = false
        val generation = downloadGeneration
        downloadButton.isEnabled = false
        downloadTask = downloads.submit {
            try {
                val value = work({ downloadCancelled || generation != downloadGeneration },
                    { bytes, total -> showDownloadProgress(generation, bytes, total) })
                if (!downloadCancelled && generation == downloadGeneration && !Thread.currentThread().isInterrupted) {
                    if (value.entries.size > 100) {
                        main.post {
                            if (!downloadCancelled && generation == downloadGeneration) {
                                downloadButton.isEnabled = true
                                chooseSubset(value)
                            }
                        }
                        return@submit
                    }
                    cache.save(value)
                    main.post {
                        if (!downloadCancelled && generation == downloadGeneration) {
                            showCatalogue(value); downloadButton.isEnabled = true
                            message.setText(R.string.download_complete)
                        }
                    }
                }
            } catch (error: ProtocolFailure) { downloadFailure(generation, error.code) }
            catch (_: java.net.SocketTimeoutException) { downloadFailure(generation, "tle_download_timeout") }
            catch (_: IOException) { downloadFailure(generation, "tle_network") }
            catch (_: SecurityException) { downloadFailure(generation, "tle_file_permission") }
        }
    }
    private fun chooseSubset(candidate: TleCatalogue) {
        val selected = mutableSetOf<Int>()
        val checked = BooleanArray(candidate.entries.size)
        val labels = candidate.entries.map { getString(R.string.local_tle_entry, it.id, it.name,
            java.time.Instant.ofEpochSecond(it.epoch).toString()) }.toTypedArray()
        val dialog = AlertDialog.Builder(this)
            .setTitle(R.string.subset_title)
            .setMultiChoiceItems(labels, checked) { source, index, isChecked ->
                if (isChecked && selected.size >= 100) {
                    (source as AlertDialog).listView.setItemChecked(index, false)
                    message.setText(R.string.subset_limit)
                } else if (isChecked) selected.add(index) else selected.remove(index)
            }
            .setPositiveButton(R.string.confirm, null)
            .setNegativeButton(R.string.cancel, null).create()
        dialog.setOnShowListener {
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                if (selected.size !in 1..100) message.setText(R.string.subset_limit)
                else {
                    val subset = TleCatalogue.subset(candidate, selected)
                    dialog.dismiss()
                    loadCatalogue { _, _ -> subset }
                }
            }
        }
        dialog.show()
        localTleInfo.text = getString(R.string.subset_explanation, candidate.entries.size)
    }
    private fun downloadFailure(generation: Int, code: String) {
        main.post {
            if (!downloadCancelled && generation == downloadGeneration) {
                downloadButton.isEnabled = true; failure(code)
            }
        }
    }
    private fun cancelDownload() {
        downloadCancelled = true; downloadGeneration++; downloadTask?.cancel(true); downloadTask = null
        if (::downloadButton.isInitialized) downloadButton.isEnabled = true
    }
    @Deprecated("Activity result API retained to avoid a runtime AndroidX dependency")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 2 && resultCode == RESULT_OK) {
            val uri = data?.data ?: return
            loadCatalogue { cancelled, progress ->
                val stream = contentResolver.openInputStream(uri) ?: throw IOException("Cannot open selected file")
                stream.use { TleCatalogue.parse(TleDownload.readBounded(it, -1, cancelled, progress), 300) }
            }
        }
    }
    private fun requestTransfer(value: TleCatalogue) {
        if (!transport.ready) { failure("not_authenticated"); return }
        if (transport.busy || transfer != null || pendingTransfer != null || downloadTask?.isDone == false) {
            message.setText(R.string.busy); return
        }
        AlertDialog.Builder(this).setMessage(R.string.transfer_replaces_catalogue)
            .setPositiveButton(R.string.confirm) { _, _ ->
                if (!transport.ready || transport.busy || transfer != null || pendingTransfer != null) {
                    message.setText(R.string.busy); return@setPositiveButton
                }
                main.removeCallbacks(passQuery); passJobActive = false
                pendingTransfer = value
                transport.command("status", JSONObject())
            }.setNegativeButton(R.string.cancel, null).show()
    }
    private fun cancelTransfer(stop: Boolean) {
        pendingTransfer = null
        val upload = transfer
        if (upload != null) {
            stopAfterTransfer = stopAfterTransfer || stop
            upload.cancel()
            localTleInfo.setText(if (upload.commitPending) R.string.transfer_commit_pending else R.string.transfer_cancel_pending)
        } else if (stop) transport.command("stop", JSONObject(), true)
    }
    override fun onStart() { super.onStart(); main.postDelayed(poll, 2000) }
    override fun onResume() {
        super.onResume()
        orbitOverview?.refreshAlertPermission()
    }
    override fun onStop() {
        main.removeCallbacks(poll); main.removeCallbacks(passQuery); cancelDownload()
        stopScan(); cancelBond(); transport.disconnect(); super.onStop()
    }
    override fun onDestroy() {
        cancelDownload(); downloads.shutdownNow()
        main.removeCallbacksAndMessages(null); unregisterReceiver(bondReceiver); super.onDestroy()
    }
    companion object {
        private const val ORBIT_NOTIFICATION_PERMISSION = 61
        private const val TRANSFER_STALL_MS = 60_000L
    }
}
