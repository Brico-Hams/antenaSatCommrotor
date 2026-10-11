package org.bricohams.portablesatstation

import android.app.Activity
import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

/**
 * Offline help shown from bundled plain-text resources (res/raw, res/raw-en, res/raw-hu).
 * No WebView, no network: the text is local and read-only.
 */
class HelpActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val column = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(24, 16, 24, 24) }
        setContentView(ScrollView(this).apply { addView(column) })
        Branding.header(this, column, Branding.Topic.MAIN, showHelp = false)
        val resource = when (intent.getStringExtra(Branding.EXTRA_TOPIC)) {
            Branding.Topic.RADIO.extra -> R.raw.help_radio
            Branding.Topic.DIGITAL.extra -> R.raw.help_digital
            else -> R.raw.help_main
        }
        column.addView(TextView(this).apply {
            text = try { resources.openRawResource(resource).use { String(it.readBytes(), Charsets.UTF_8) } }
                   catch (_: java.io.IOException) { getString(R.string.help_unavailable) }
            textSize = 15f
            setTextIsSelectable(true)
            setPadding(0, 16, 0, 16)
        })
        column.addView(Button(this).apply { setText(R.string.digital_back); setOnClickListener { finish() } })
    }
}
