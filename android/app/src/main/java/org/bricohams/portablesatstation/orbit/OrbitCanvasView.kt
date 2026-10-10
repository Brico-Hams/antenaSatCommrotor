package org.bricohams.portablesatstation.orbit

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.view.View
import kotlin.math.abs
import kotlin.math.min

internal class OrbitCanvasView(context: Context) : View(context) {
    var snapshot: OrbitSnapshot? = null
        set(value) { field = value; invalidate() }
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val density = resources.displayMetrics.density
    private fun line(canvas: Canvas, x1: Float, y1: Float, x2: Float, y2: Float, color: Int) {
        paint.color = color; paint.strokeWidth = density
        canvas.drawLine(x1, y1, x2, y2, paint)
    }
    private fun text(canvas: Canvas, value: String, x: Float, y: Float) {
        paint.color = Color.LTGRAY; paint.textSize = 11 * density
        canvas.drawText(value, x, y, paint)
    }
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        canvas.drawColor(Color.rgb(15, 24, 36))
        val left = 28 * density; val top = 34 * density
        val mapWidth = width - left - 16 * density
        if (mapWidth <= 0) return
        val mapHeight = mapWidth / 2
        text(canvas, "Offline schematic global coordinates — not a street map", 8 * density, 17 * density)
        for (lon in -180..180 step 30) {
            val x = left + (lon + 180) / 360f * mapWidth
            line(canvas, x, top, x, top + mapHeight, Color.DKGRAY)
        }
        for (lat in -90..90 step 30) {
            val y = top + (90 - lat) / 180f * mapHeight
            line(canvas, left, y, left + mapWidth, y, Color.DKGRAY)
        }
        text(canvas, "90°N", 0f, top + 4 * density)
        text(canvas, "0°", 0f, top + mapHeight / 2)
        text(canvas, "90°S", 0f, top + mapHeight)
        text(canvas, "180°W", left, top + mapHeight + 14 * density)
        text(canvas, "0°", left + mapWidth / 2, top + mapHeight + 14 * density)
        text(canvas, "180°E", left + mapWidth - 35 * density, top + mapHeight + 14 * density)
        fun map(point: GeoPoint): Pair<Float, Float> {
            val projected = OrbitGeometry.project(point)
            return Pair(left + projected.first.toFloat() * mapWidth, top + projected.second.toFloat() * mapHeight)
        }
        snapshot?.groundTrack?.zipWithNext()?.forEach { (a, b) ->
            // Do not draw a spurious line across the whole world at the date line.
            if (abs(a.point.longitude - b.point.longitude) <= 180) {
                val p = map(a.point); val q = map(b.point)
                line(canvas, p.first, p.second, q.first, q.second, Color.CYAN)
            }
        }
        snapshot?.subpoint?.let {
            val p = map(it.point); paint.color = Color.YELLOW
            canvas.drawCircle(p.first, p.second, 5 * density, paint)
        }
        snapshot?.observer?.let {
            val p = map(it.point); paint.color = Color.GREEN
            canvas.drawCircle(p.first, p.second, 4 * density, paint)
        }
        val radarTop = top + mapHeight + 52 * density
        val radius = min(mapWidth / 2 - 24 * density, (height - radarTop - 28 * density) / 2)
        if (radius <= 0) return
        val cx = width / 2f; val cy = radarTop + radius
        text(canvas, "AZ/EL radar • cyan host path • yellow sample • magenta measured POL", 8 * density, radarTop - 13 * density)
        paint.color = Color.DKGRAY; paint.style = Paint.Style.STROKE
        for (ring in 1..3) canvas.drawCircle(cx, cy, radius * ring / 3, paint)
        paint.style = Paint.Style.FILL
        line(canvas, cx - radius, cy, cx + radius, cy, Color.DKGRAY)
        line(canvas, cx, cy - radius, cx, cy + radius, Color.DKGRAY)
        text(canvas, "N", cx - 4 * density, cy - radius - 4 * density)
        text(canvas, "E", cx + radius + 4 * density, cy)
        text(canvas, "S", cx, cy + radius + 14 * density)
        text(canvas, "W", cx - radius - 14 * density, cy)
        text(canvas, "90°", cx + 4 * density, cy - 4 * density)
        fun sky(point: RadarPoint): Pair<Float, Float>? = OrbitGeometry.radar(point)?.let {
            Pair(cx + it.first.toFloat() * radius, cy + it.second.toFloat() * radius)
        }
        snapshot?.radarTrack?.zipWithNext()?.forEach { (a, b) ->
            val p = sky(a); val q = sky(b)
            if (p != null && q != null) line(canvas, p.first, p.second, q.first, q.second, Color.CYAN)
        }
        snapshot?.tracking?.let { sample ->
            sky(sample)?.let { p ->
                paint.color = Color.YELLOW; canvas.drawCircle(p.first, p.second, 5 * density, paint)
                snapshot?.measuredAxes?.let { axes ->
                    val pol = Math.toRadians(axes.polDegrees)
                    val dx = kotlin.math.sin(pol).toFloat() * 13 * density
                    val dy = -kotlin.math.cos(pol).toFloat() * 13 * density
                    line(canvas, p.first - dx, p.second - dy, p.first + dx, p.second + dy, Color.MAGENTA)
                }
            }
        }
    }
}
