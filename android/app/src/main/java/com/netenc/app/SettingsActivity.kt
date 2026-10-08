package com.netenc.app

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.Switch
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class SettingsActivity : AppCompatActivity() {
    companion object {
        const val DEFAULT_TOKEN = "09136555866"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getSharedPreferences("netenc", MODE_PRIVATE)

        val host = EditText(this).apply {
            hint = "آدرس API ویندوز (http://IP:5050)"
            setText(prefs.getString("host", ""))
            layoutDirection = android.view.View.LAYOUT_DIRECTION_LTR
            textAlignment = android.view.View.TEXT_ALIGNMENT_VIEW_START
        }
        val token = EditText(this).apply {
            hint = "توکن API"
            setText(prefs.getString("token", DEFAULT_TOKEN) ?: DEFAULT_TOKEN)
            inputType = android.text.InputType.TYPE_CLASS_TEXT or
                android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD
        }
        val autoSync = Switch(this).apply {
            text = "همگام‌سازی خودکار هنگام ورود"
            isChecked = prefs.getBoolean("auto_sync", false)
        }
        val save = Button(this).apply {
            text = "ذخیره تنظیمات"
            setOnClickListener {
                prefs.edit()
                    .putString("host", host.text.toString().trim())
                    .putString("token", token.text.toString())
                    .putBoolean("auto_sync", autoSync.isChecked)
                    .apply()
                Toast.makeText(this@SettingsActivity, "ذخیره شد", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
        val sourcesBtn = Button(this).apply {
            text = "منابع معتبر (افزودن / حذف لینک)"
            setOnClickListener {
                startActivity(Intent(this@SettingsActivity, SourcesActivity::class.java))
            }
        }
        val note = TextView(this).apply {
            text = """
                Engineer Jokar · 09136555866

                توکن پیش‌فرض با ویندوز یکسان است.
                روی ویندوز: start.bat (NETENC_TOKEN=09136555866)

                API:
                /api/stats  /api/chapters  /api/search
                /api/scenarios  /api/reseed  /api/sync/*
                /api/sources
            """.trimIndent()
            setPadding(8, 24, 8, 8)
            textSize = 13f
        }

        val inner = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(28, 28, 28, 28)
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            addView(TextView(this@SettingsActivity).apply {
                text = "تنظیمات و API"
                textSize = 20f
                setPadding(0, 0, 0, 16)
            })
            addView(host)
            addView(token)
            addView(autoSync)
            addView(save)
            addView(sourcesBtn)
            addView(note)
        }
        setContentView(ScrollView(this).apply { addView(inner) })
    }
}
