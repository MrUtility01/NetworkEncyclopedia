package com.netenc.app

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.text.InputType
import android.view.Gravity
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

/**
 * ورود اجباری با رمز برنامه.
 * رمز: engineerjokar
 */
class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getSharedPreferences("netenc", MODE_PRIVATE)
        // اگر قبلاً با رمز قدیم unlock شده، با رمز جدید دوباره بخواهد
        val savedToken = prefs.getString("token", "")
        if (prefs.getBoolean("unlocked", false) && savedToken == APP_PASSWORD) {
            goMain()
            return
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setBackgroundColor(Color.parseColor("#F4F6F9"))
            setPadding(48, 48, 48, 48)
        }
        root.addView(TextView(this).apply {
            text = "Network Engineer"
            textSize = 24f
            setTextColor(Color.parseColor("#1D4ED8"))
            gravity = Gravity.CENTER
        })
        root.addView(TextView(this).apply {
            text = "رمز ورود برنامه را وارد کنید"
            textSize = 14f
            setTextColor(Color.parseColor("#64748B"))
            gravity = Gravity.CENTER
            setPadding(0, 24, 0, 16)
        })
        val pass = EditText(this).apply {
            hint = "رمز"
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            setPadding(32, 28, 32, 28)
            setBackgroundColor(Color.WHITE)
        }
        root.addView(pass, LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply { setMargins(0, 8, 0, 16) })
        root.addView(Button(this).apply {
            text = "ورود"
            setOnClickListener {
                val ok = pass.text?.toString()?.trim() == APP_PASSWORD
                if (ok) {
                    prefs.edit()
                        .putBoolean("unlocked", true)
                        .putString("token", APP_PASSWORD)
                        .apply()
                    goMain()
                } else {
                    Toast.makeText(this@LoginActivity, "رمز نادرست است", Toast.LENGTH_SHORT).show()
                }
            }
        })
        setContentView(root)
    }

    private fun goMain() {
        startActivity(Intent(this, MainActivity::class.java))
        finish()
    }

    companion object {
        const val APP_PASSWORD = "engineerjokar"
    }
}
