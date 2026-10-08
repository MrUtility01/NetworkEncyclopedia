package com.netenc.app

import android.content.Context
import android.graphics.Color
import android.graphics.Typeface
import android.util.TypedValue
import android.view.View
import android.widget.TextView

/** تم روشن حرفه‌ای — خوانا برای فارسی */
object Ui {
    val BG = Color.parseColor("#F4F6F9")
    val CARD = Color.parseColor("#FFFFFF")
    val TEXT = Color.parseColor("#1B2430")
    val MUTED = Color.parseColor("#5A6A7A")
    val ACCENT = Color.parseColor("#1D4ED8")
    val ACCENT_SOFT = Color.parseColor("#DBEAFE")
    val BORDER = Color.parseColor("#D8DEE8")
    val SUCCESS = Color.parseColor("#166534")
    val DANGER = Color.parseColor("#B91C1C")
    val WARN = Color.parseColor("#C2410C")

    fun persianTypeface(): Typeface =
        Typeface.create("sans-serif", Typeface.NORMAL)

    fun text(ctx: Context, msg: String, sizeSp: Float = 14f, color: Int = TEXT): TextView =
        TextView(ctx).apply {
            text = msg
            setTextColor(color)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, sizeSp)
            typeface = persianTypeface()
            textDirection = View.TEXT_DIRECTION_RTL
            layoutDirection = View.LAYOUT_DIRECTION_RTL
            setTextIsSelectable(true)
            setPadding(dp(ctx, 12), dp(ctx, 8), dp(ctx, 12), dp(ctx, 8))
        }

    fun dp(ctx: Context, v: Int): Int =
        (v * ctx.resources.displayMetrics.density).toInt()
}
