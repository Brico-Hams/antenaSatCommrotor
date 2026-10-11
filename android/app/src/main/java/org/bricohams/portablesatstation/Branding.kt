package org.bricohams.portablesatstation

import android.app.Activity
import android.content.Intent
import android.text.util.Linkify
import android.text.method.LinkMovementMethod
import android.view.Gravity
import android.widget.Button
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView

/** BricoHams logo, authors line and context help entry shared by every screen. */
object Branding {
    const val EXTRA_TOPIC = "help_topic"
    enum class Topic(val extra: String) { MAIN("main"), RADIO("radio"), DIGITAL("digital") }

    fun header(activity: Activity, parent: LinearLayout, topic: Topic, showHelp: Boolean = true) {
        val logo = ImageView(activity).apply {
            setImageResource(R.drawable.bricohams_logo)
            adjustViewBounds = true
            maxHeight = (96 * activity.resources.displayMetrics.density).toInt()
            contentDescription = activity.getString(R.string.logo_description)
            importantForAccessibility = android.view.View.IMPORTANT_FOR_ACCESSIBILITY_YES
        }
        parent.addView(logo, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT).apply { bottomMargin = 8 })
        parent.addView(TextView(activity).apply {
            text = activity.getString(R.string.credits)
            gravity = Gravity.CENTER_HORIZONTAL
            textSize = 12f
            autoLinkMask = Linkify.WEB_URLS
            movementMethod = LinkMovementMethod.getInstance()
        })
        if (showHelp) parent.addView(Button(activity).apply {
            setText(R.string.help_open)
            setOnClickListener {
                activity.startActivity(Intent(activity, HelpActivity::class.java).putExtra(EXTRA_TOPIC, topic.extra))
            }
        })
    }
}
