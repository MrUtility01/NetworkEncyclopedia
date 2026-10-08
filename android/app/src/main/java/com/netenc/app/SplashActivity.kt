package com.netenc.app

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class SplashActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setBackgroundColor(Color.parseColor("#F4F6F9"))
            setPadding(48, 48, 48, 48)
        }
        root.addView(TextView(this).apply {
            text = "Network Encyclopedia"
            textSize = 26f
            setTextColor(Color.parseColor("#1D4ED8"))
            gravity = Gravity.CENTER
        })
        root.addView(TextView(this).apply {
            text = "دانشنامه شبکه و زیرساخت"
            textSize = 16f
            setTextColor(Ui.TEXT)
            gravity = Gravity.CENTER
            setPadding(0, 16, 0, 8)
        })
        root.addView(TextView(this).apply {
            text = "آفلاین · ۶۳ فصل · یادگیری عمیق"
            textSize = 13f
            setTextColor(Ui.MUTED)
            gravity = Gravity.CENTER
        })
        setContentView(root)
        Handler(Looper.getMainLooper()).postDelayed({
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        }, 900)
    }
}
