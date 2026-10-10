package org.bricohams.portablesatstation.orbit

import android.content.Context
import android.app.AlertDialog
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import org.json.JSONObject
import java.time.Instant
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter

/** Programmatic native UI. All displayed orbit/RF values originate in submitSnapshot(), not demo data. */
class SatelliteOverviewView(context: Context) : ScrollView(context) {
    var onHostRouteRequested: ((String, String, JSONObject) -> Unit)? = null
    var onSatelliteSelected: ((Int) -> Unit)? = null
        set(value) { field = value; renderCatalogue() }
    var onAxesRequested: ((ThreeAxisState) -> Unit)? = null
        set(value) { field = value; updateFreshness() }
    /** Activity owns requestPermissions(); never request permission until the user taps the button. */
    var onNotificationPermissionRequested: (() -> Unit)? = null
    private val root = LinearLayout(context).apply { orientation = LinearLayout.VERTICAL }
    private val prefs = context.getSharedPreferences("orbit_favorites", Context.MODE_PRIVATE)
    private val alerts = PassAlerts(context)
    private val status = TextView(context)
    private val alertStatus = TextView(context)
    private val detail = TextView(context)
    private val passes = TextView(context)
    private val radio = TextView(context)
    private val hostReply = TextView(context)
    private val catalogue = LinearLayout(context).apply { orientation = LinearLayout.VERTICAL }
    private val query = EditText(context).apply {
        hint = "Filter satellite name / NORAD ID"
        filters = arrayOf(android.text.InputFilter.LengthFilter(128))
        setSingleLine()
    }
    private val favoriteFilter = CheckBox(context).apply { text = "Favorites only (local device)" }
    private val alertOptIn = CheckBox(context).apply { text = "Opt in to best-effort AOS alert for selected satellite" }
    private val canvas = OrbitCanvasView(context)
    private val az = axisField("Requested AZ (0…360°)")
    private val el = axisField("Requested EL (−90…90°)")
    private val pol = axisField("Requested mechanical POL (−180…180°)")
    private val requestAxes = Button(context).apply { text = "Request AZ / EL / POL from host" }
    private var current: OrbitSnapshot? = null
    private var updating = false
    private val clock = object : Runnable {
        override fun run() { updateFreshness(); postDelayed(this, 5000) }
    }
    init {
        root.setPadding(16, 16, 16, 16)
        addView(root)
        root.addView(status)
        root.addView(query); root.addView(favoriteFilter); root.addView(catalogue)
        root.addView(detail)
        root.addView(canvas, LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, (560 * resources.displayMetrics.density).toInt()))
        root.addView(passes)
        root.addView(alertOptIn); root.addView(alertStatus)
        root.addView(Button(context).apply {
            text = "Allow AOS notifications (Android permission)"
            setOnClickListener {
                if (alerts.hasPermission()) alertStatus.text = alerts.permissionStatus()
                else if (onNotificationPermissionRequested != null) onNotificationPermissionRequested?.invoke()
                else alertStatus.text = "Permission request unavailable: Activity integration pending"
            }
        })
        root.addView(radio)
        root.addView(TextView(context).apply {
            text = "POL is a mechanical third-axis angle, not an RHCP/LHCP selector. RF acknowledgement is not proof of radiated frequency."
        })
        root.addView(az); root.addView(el); root.addView(pol); root.addView(requestAxes)
        requestAxes.setOnClickListener {
            try {
                check(current?.isFresh(now()) == true && onAxesRequested != null)
                val target = ThreeAxisState(az.text.toString().toDouble(), el.text.toString().toDouble(), pol.text.toString().toDouble())
                onAxesRequested?.invoke(target)
                status.text = "Axis request sent to adapter; await actual host acknowledgement/measurements"
            } catch (_: IllegalArgumentException) { status.text = "Enter finite AZ 0…360, EL −90…90, POL −180…180 degrees" }
              catch (_: IllegalStateException) { status.text = "Fresh host data and axis adapter required" }
        }
        query.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) { renderCatalogue() }
            override fun afterTextChanged(s: Editable?) {}
        })
        favoriteFilter.setOnCheckedChangeListener { _, _ -> renderCatalogue() }
        alertOptIn.setOnCheckedChangeListener { _, checked ->
            if (!updating) selected()?.let { sat ->
                alertStatus.text = alerts.setEnabled(sat, checked, nextPass(), now())
            }
        }
        render()
        addHostApiControls()
    }

    private fun addHostApiControls() {
        root.addView(TextView(context).apply {
            text = "CM5 rotor host API · authenticated radio-host session only"
            textSize = 18f
        })
        root.addView(TextView(context).apply {
            text = "Responses are shown as host data; this app does not convert them into an OrbitSnapshot, derive passes locally, or claim axis feedback."
        })
        hostButton("/rotor/status", "get")
        hostButton("/rotor/sensorsstatus", "get")
        hostButton("/satellites/catalog", "get")

        val norad = EditText(context).apply {
            hint = "NORAD ID (from host catalogue)"
            inputType = android.text.InputType.TYPE_CLASS_NUMBER
            setSingleLine()
        }
        root.addView(norad)
        hostButton("/satellites/passes", "get") {
            val id = norad.text.toString().toIntOrNull()
            if (id == null) {
                hostReply.text = "Unsupported request: enter a valid integer NORAD ID."
                return@hostButton
            }
            requestHost("/satellites/passes", "get", JSONObject().put("noradId", id).put("limit", 10))
        }
        hostButton("/rotor/track", "set") {
            val id = norad.text.toString().toIntOrNull()
            if (id == null) {
                hostReply.text = "Unsupported request: enter a valid integer NORAD ID."
                return@hostButton
            }
            confirmHostRequest("/rotor/track", JSONObject().put("noradId", id))
        }
        hostButton("/rotor/target", "set") {
            try {
                val target = ThreeAxisState(
                    az.text.toString().toDouble(),
                    el.text.toString().toDouble(),
                    pol.text.toString().toDouble()
                )
                confirmHostRequest("/rotor/target", JSONObject()
                    .put("azDeg", target.azimuthDegrees)
                    .put("elDeg", target.elevationDegrees)
                    .put("polDeg", target.polDegrees))
            } catch (_: IllegalArgumentException) {
                hostReply.text = "Unsupported request: enter finite AZ, EL and mechanical POL values in range."
            }
        }
        hostButton("/rotor/stop", "set") {
            confirmHostRequest("/rotor/stop", JSONObject(), "Stop rotor motion/tracking?")
        }
        root.addView(TextView(context).apply {
            text = "Remote /rotor/home and /rotor/calibrate are not exposed here: the CM5 contract requires trusted local-console confirmation for these operations."
        })
        root.addView(hostReply)
    }

    private fun hostButton(
        path: String,
        operation: String,
        action: (() -> Unit)? = null
    ) {
        root.addView(Button(context).apply {
            text = "$operation $path"
            setOnClickListener {
                if (action != null) action()
                else requestHost(path, operation, JSONObject())
            }
        })
    }

    private fun confirmHostRequest(
        path: String,
        data: JSONObject,
        prompt: String = "Send this command to the CM5 rotor host?"
    ) {
        AlertDialog.Builder(context)
            .setMessage(prompt)
            .setPositiveButton("Confirm") { _, _ -> requestHost(path, "set", data) }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun requestHost(path: String, operation: String, data: JSONObject) {
        val error = RotorHostApi.requestError(path, operation, data)
        if (error != null) {
            hostReply.text = "Unsupported request: $error"
            return
        }
        val callback = onHostRouteRequested
        if (callback == null) {
            hostReply.text = "Host API unavailable: connect and authenticate the CM5 radio host."
            return
        }
        hostReply.text = "Waiting for host response: $operation $path"
        callback(path, operation, data)
    }

    /** Displays only data returned by a schema-validated CM5 rotor route. */
    fun submitHostRouteResult(path: String, data: JSONObject?, error: String?) {
        check(android.os.Looper.myLooper() == android.os.Looper.getMainLooper())
        hostReply.text = when {
            error != null -> "Host error for $path: $error"
            data != null -> "$path\n${data.toString(2)}"
            else -> "Host error for $path: response has neither data nor an explicit error"
        }
    }
    private fun axisField(hintText: String) = EditText(context).apply {
        hint = hintText; setSingleLine()
        inputType = android.text.InputType.TYPE_CLASS_NUMBER or
            android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL or android.text.InputType.TYPE_NUMBER_FLAG_SIGNED
        filters = arrayOf(android.text.InputFilter.LengthFilter(16))
    }
    /** Must run on the UI thread. null clears data and cancels scheduled alerts without erasing opt-ins. */
    fun submitSnapshot(snapshot: OrbitSnapshot?) {
        check(android.os.Looper.myLooper() == android.os.Looper.getMainLooper())
        if (current?.selectedNoradId != snapshot?.selectedNoradId) current?.selectedNoradId?.let(alerts::cancel)
        current = snapshot; canvas.snapshot = snapshot
        render()
    }
    /** Activity calls after POST_NOTIFICATIONS result and on resume (also refreshes revoked permissions). */
    fun refreshAlertPermission() { updateFreshness() }
    private fun now() = System.currentTimeMillis() / 1000
    private fun selected() = current?.let { snapshot -> snapshot.catalogue.find { it.noradId == snapshot.selectedNoradId } }
    private fun nextPass(): OrbitPass? = current?.takeIf { it.isFresh(now()) }?.passes?.firstOrNull {
        OrbitGeometry.alertEligible(it, now())
    }
    private fun favorites(): Set<Int> = prefs.getStringSet("norad_ids", emptySet()).orEmpty().mapNotNull { it.toIntOrNull() }.toSet()
    private fun renderCatalogue() {
        catalogue.removeAllViews()
        val snapshot = current ?: return
        val favorites = favorites()
        val entries = OrbitGeometry.filtered(snapshot.catalogue, query.text.toString(), favoriteFilter.isChecked, favorites)
        if (entries.isEmpty()) catalogue.addView(TextView(context).apply { text = "No matching supplied catalogue entries" })
        entries.forEach { sat ->
            val row = LinearLayout(context)
            row.addView(Button(context).apply {
                text = "${if (sat.noradId == snapshot.selectedNoradId) "• " else ""}${sat.name} [${sat.noradId}]"
                isEnabled = onSatelliteSelected != null
                setOnClickListener { onSatelliteSelected?.invoke(sat.noradId) }
            }, LinearLayout.LayoutParams(0, LayoutParams.WRAP_CONTENT, 1f))
            row.addView(CheckBox(context).apply {
                text = "★"; contentDescription = "Favorite ${sat.name}"; isChecked = sat.noradId in favorites
                setOnCheckedChangeListener { _, checked ->
                    val ids = favorites().toMutableSet()
                    if (checked) ids.add(sat.noradId) else ids.remove(sat.noradId)
                    prefs.edit().putStringSet("norad_ids", ids.map { it.toString() }.toSet()).apply()
                    renderCatalogue()
                }
            })
            catalogue.addView(row)
        }
    }
    private fun time(value: Long) = DateTimeFormatter.ofPattern("uuuu-MM-dd HH:mm:ss 'UTC'")
        .withZone(ZoneOffset.UTC).format(Instant.ofEpochSecond(value))
    private fun hz(value: Long?) = value?.let { "$it Hz" } ?: "unknown"
    private fun axes(value: ThreeAxisState?) = value?.let {
        "AZ ${it.azimuthDegrees}° / EL ${it.elevationDegrees}° / POL ${it.polDegrees}°"
    } ?: "unavailable"
    private fun render() {
        renderCatalogue()
        val s = current
        detail.text = if (s == null) "Integration pending: no host snapshot supplied" else buildString {
            append("${selected()?.name ?: "No selection"} • observer: ${s.observer?.name ?: "unknown"}\n")
            s.observer?.let { append("Site ${it.point.latitude}°, ${it.point.longitude}°, ${it.altitudeMeters} m\n") }
            append("Source generated ${time(s.generatedUtc)}; valid until ${time(s.validUntilUtc)}\n")
            s.subpoint?.let { append("Subpoint ${it.point.latitude}°, ${it.point.longitude}° at ${time(it.utcSeconds)}\n") }
                ?: append("Subpoint unavailable; no fabricated orbit\n")
            s.tracking?.let { append("Tracking AZ ${it.azimuthDegrees}° EL ${it.elevationDegrees}° at ${time(it.utcSeconds)}\n") }
            append("Measured ${axes(s.measuredAxes)}\nHost-requested ${axes(s.requestedAxes)}")
        }
        passes.text = s?.passes?.joinToString("\n", prefix = "Supplied passes (UTC)\n") {
            "AOS ${time(it.aosUtc)} • peak ${time(it.peakUtc)} • LOS ${time(it.losUtc)} • max EL ${it.maxElevation}°${if (it.partial) " • partial (no alert)" else ""}"
        }?.takeIf { s.passes.isNotEmpty() } ?: "No host-calculated passes supplied"
        radio.text = s?.radioProfiles?.joinToString("\n\n", prefix = "Explicit supplied radio profiles / Doppler requests\n") {
            "${it.name} • ${it.mode} • ${if (it.supported) "adapter reports supported" else "unsupported"}\n" +
                "Nominal UL ${hz(it.uplinkHz)} / DL ${hz(it.downlinkHz)}\n" +
                "Requested UL ${hz(it.requestedUplinkHz)} / DL ${hz(it.requestedDownlinkHz)}\n" +
                "RF adapter acknowledged UL ${hz(it.acknowledgedUplinkHz)} / DL ${hz(it.acknowledgedDownlinkHz)}"
        }?.takeIf { s.radioProfiles.isNotEmpty() } ?: "No radio profile supplied; frequency/mode unknown"
        updating = true
        alertOptIn.isEnabled = selected() != null
        alertOptIn.isChecked = selected()?.let { alerts.enabled(it.noradId) } ?: false
        updating = false
        updateFreshness()
    }
    private fun updateFreshness() {
        val fresh = current?.isFresh(now()) == true
        status.text = when {
            current == null -> "NOT LIVE — host integration pending"
            fresh -> "Fresh supplied host snapshot (no on-phone orbit propagation)"
            else -> "STALE / OFFLINE supplied data — not live tracking"
        }
        requestAxes.isEnabled = fresh && onAxesRequested != null
        if (!fresh) alerts.cancelAllScheduled()
        alertStatus.text = selected()?.let { alerts.reconcile(it, nextPass(), now()) } ?: alerts.permissionStatus()
        canvas.contentDescription = "${status.text}. Schematic coordinate map and host AZ/EL path; measured POL in magenta."
    }
    override fun onAttachedToWindow() { super.onAttachedToWindow(); removeCallbacks(clock); post(clock); renderCatalogue() }
    override fun onDetachedFromWindow() { removeCallbacks(clock); super.onDetachedFromWindow() }
}
