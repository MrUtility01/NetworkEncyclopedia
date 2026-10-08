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
            setBackgroundColor(Color.parseColor("#0B1220"))
            setPadding(48, 48, 48, 48)
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
        }
        val logo = TextView(this).apply {
            text = "EJ"
            textSize = 56f
            setTextColor(Color.parseColor("#3B82F6"))
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 16)
        }
        val brand = TextView(this).apply {
            text = "Engineer Jokar"
            textSize = 26f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
        }
        val sub = TextView(this).apply {
            text = "دایرةالمعارف شبکه و زیرساخت"
            textSize = 15f
            setTextColor(Color.parseColor("#9AA8BC"))
            gravity = Gravity.CENTER
            setPadding(0, 12, 0, 8)
        }
        val phone = TextView(this).apply {
            text = "09132184122"
            textSize = 18f
            setTextColor(Color.parseColor("#93C5FD"))
            gravity = Gravity.CENTER
            setPadding(0, 24, 0, 0)
        }
        val ver = TextView(this).apply {
            text = "NetEnc · Offline + Sync"
            textSize = 12f
            setTextColor(Color.parseColor("#64748B"))
            gravity = Gravity.CENTER
            setPadding(0, 40, 0, 0)
        }
        root.addView(logo)
        root.addView(brand)
        root.addView(sub)
        root.addView(phone)
        root.addView(ver)
        setContentView(root)

        Handler(Looper.getMainLooper()).postDelayed({
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        }, 1800)
    }
}
