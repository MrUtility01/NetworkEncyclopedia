package com.netenc.app

import android.content.Context
import android.graphics.Color
import android.graphics.Typeface
import android.util.TypedValue
import android.view.View
import android.widget.TextView

object Ui {
    val BG = Color.parseColor("#0F1419")
    val CARD = Color.parseColor("#1A2332")
    val TEXT = Color.parseColor("#E8EEF7")
    val MUTED = Color.parseColor("#9AA8BC")
    val ACCENT = Color.parseColor("#60A5FA")

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
