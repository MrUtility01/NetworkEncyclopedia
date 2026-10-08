package com.netenc.app

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Switch
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class SettingsActivity : AppCompatActivity() {
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
            hint = "توکن API (اختیاری)"
            setText(prefs.getString("token", ""))
            inputType = android.text.InputType.TYPE_CLASS_TEXT or android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD
        }
        val autoSync = Switch(this).apply {
            text = "همگام‌سازی خودکار هنگام ورود (اگر سرور در دسترس باشد)"
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
        val note = TextView(this).apply {
            text = "Engineer Jokar · 09132184122\n\nAPI ویندوز:\n/api/stats  /api/chapters  /api/search\n/api/scenarios  /api/reseed  /api/sync/*"
            setPadding(8, 24, 8, 8)
            textSize = 13f
        }

        val root = LinearLayout(this).apply {
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
            addView(note)
        }
        setContentView(root)
    }
}
