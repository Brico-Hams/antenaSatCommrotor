package org.bricohams.portablesatstation.orbit

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager

class PassAlertReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != PassAlerts.ACTION) return
        if (android.os.Build.VERSION.SDK_INT >= 33 &&
            context.checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) !=
            PackageManager.PERMISSION_GRANTED) return
        val id = intent.getIntExtra("noradId", 0)
        val aos = intent.getLongExtra("aosUtc", 0)
        val name = intent.getStringExtra("name") ?: return
        if (id !in 1..999999999 || name.isBlank() || name.length > 128) return
        val prefs = context.getSharedPreferences("orbit_pass_alerts", Context.MODE_PRIVATE)
        if (!prefs.getBoolean("enabled_$id", false) || prefs.getLong("aos_$id", 0) != aos) return
        val now = System.currentTimeMillis() / 1000
        // Suppress obsolete delayed alarms rather than announcing a pass long after it happened.
        if (now < aos || now - aos > 900) return
        if (!PassAlerts(context).hasPermission()) return
        val manager = context.getSystemService(NotificationManager::class.java)
        if (!manager.areNotificationsEnabled()) return
        manager.createNotificationChannel(NotificationChannel(PassAlerts.CHANNEL, "Satellite AOS", NotificationManager.IMPORTANCE_DEFAULT))
        try {
            manager.notify(id, android.app.Notification.Builder(context, PassAlerts.CHANNEL)
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentTitle("$name — predicted AOS")
                .setContentText("Host-predicted pass time. Alert may be delayed; verify tracking before operating.")
                .setAutoCancel(true).build())
            prefs.edit().remove("aos_$id").apply()
        } catch (_: SecurityException) { /* Permission can be revoked between check and delivery. */ }
    }
}
