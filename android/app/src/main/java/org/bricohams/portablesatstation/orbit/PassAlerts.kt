package org.bricohams.portablesatstation.orbit

import android.Manifest
import android.app.AlarmManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build

/** Opt-in, best-effort inexact AOS alerts. No background networking or exact-alarm permission. */
class PassAlerts(private val context: Context) {
    private val prefs = context.getSharedPreferences("orbit_pass_alerts", Context.MODE_PRIVATE)
    private val alarms = context.getSystemService(AlarmManager::class.java)
    fun enabled(noradId: Int) = prefs.getBoolean("enabled_$noradId", false)
    fun hasPermission() = Build.VERSION.SDK_INT < 33 ||
        context.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED
    fun permissionStatus(): String {
        val manager = context.getSystemService(NotificationManager::class.java)
        if (!receiverRegistered()) return "AOS integration pending: private receiver not registered"
        if (!hasPermission()) return "Notification permission required (Android 13+)"
        if (!manager.areNotificationsEnabled()) return "Notifications disabled in Android settings"
        if (manager.getNotificationChannel(CHANNEL)?.importance == NotificationManager.IMPORTANCE_NONE)
            return "AOS channel disabled in Android settings"
        return "Best-effort inexact AOS alerts; Android may delay delivery"
    }
    private fun receiverRegistered(): Boolean = try {
        !context.packageManager.getReceiverInfo(ComponentName(context, PassAlertReceiver::class.java), 0).exported
    } catch (_: PackageManager.NameNotFoundException) { false }
    private fun pending(noradId: Int, aos: Long = 0, name: String = ""): PendingIntent =
        PendingIntent.getBroadcast(context, noradId,
            Intent(context, PassAlertReceiver::class.java)
                .setAction(ACTION).setData(Uri.parse("portablesatstation://aos/$noradId"))
                .putExtra("noradId", noradId).putExtra("aosUtc", aos).putExtra("name", name),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)

    fun setEnabled(satellite: OrbitSatellite, enabled: Boolean, pass: OrbitPass?, nowUtc: Long): String {
        prefs.edit().putBoolean("enabled_${satellite.noradId}", enabled).apply()
        return reconcile(satellite, pass, nowUtc)
    }
    fun cancel(noradId: Int) {
        alarms.cancel(pending(noradId))
        context.getSystemService(NotificationManager::class.java).cancel(noradId)
        prefs.edit().remove("aos_$noradId").apply()
    }
    fun cancelAllScheduled() {
        prefs.all.keys.filter { it.startsWith("aos_") }.forEach {
            it.removePrefix("aos_").toIntOrNull()?.let(::cancel)
        }
    }
    /** Call on new host predictions, disconnect, selection change, and UI resume. */
    fun reconcile(satellite: OrbitSatellite, pass: OrbitPass?, nowUtc: Long): String {
        val id = satellite.noradId
        if (!enabled(id)) { cancel(id); return "AOS alerts off" }
        if (!receiverRegistered()) { cancel(id); return permissionStatus() }
        if (!hasPermission() || !context.getSystemService(NotificationManager::class.java).areNotificationsEnabled()) {
            cancel(id); return permissionStatus()
        }
        if (pass == null || !OrbitGeometry.alertEligible(pass, nowUtc)) {
            cancel(id); return "No fresh complete future pass available; no alert scheduled"
        }
        val manager = context.getSystemService(NotificationManager::class.java)
        manager.createNotificationChannel(NotificationChannel(CHANNEL, "Satellite AOS", NotificationManager.IMPORTANCE_DEFAULT))
        if (manager.getNotificationChannel(CHANNEL)?.importance == NotificationManager.IMPORTANCE_NONE) {
            cancel(id); return permissionStatus()
        }
        if (prefs.getLong("aos_$id", 0) != pass.aosUtc) {
            cancel(id)
            try {
                alarms.set(AlarmManager.RTC_WAKEUP, pass.aosUtc * 1000, pending(id, pass.aosUtc, satellite.name))
                prefs.edit().putLong("aos_$id", pass.aosUtc).apply()
            } catch (_: SecurityException) {
                return "Android rejected alert scheduling; no alert scheduled"
            }
        }
        return "Inexact AOS alert requested; delivery not guaranteed"
    }
    companion object {
        internal const val CHANNEL = "orbit_aos"
        internal const val ACTION = "org.bricohams.portablesatstation.orbit.AOS"
    }
}
