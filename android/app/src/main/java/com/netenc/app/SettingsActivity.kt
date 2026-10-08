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
    companion object { const val DEFAULT_TOKEN = "09136555866" }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getSharedPreferences("netenc", MODE_PRIVATE)
        fun field(hint: String, key: String, password: Boolean = false, def: String = "") =
            EditText(this).apply {
                this.hint = hint
                setText(prefs.getString(key, def) ?: def)
                if (password) inputType = android.text.InputType.TYPE_CLASS_TEXT or android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD
                layoutDirection = android.view.View.LAYOUT_DIRECTION_LTR
                textAlignment = android.view.View.TEXT_ALIGNMENT_VIEW_START
            }
        val host = field("API ویندوز http://IP:5050", "host")
        val token = field("توکن API", "token", true, DEFAULT_TOKEN)
        val autoSync = Switch(this).apply { text = "همگام خودکار"; isChecked = prefs.getBoolean("auto_sync", false) }
        val aiProvider = field("AI: openai | grok | openai-compat", "ai_provider", def = "openai")
        val aiBase = field("Base URL", "ai_base", def = "https://api.openai.com/v1")
        val aiKey = field("کلید API هوش مصنوعی", "ai_api_key", true)
        val aiModel = field("مدل", "ai_model", def = "gpt-4o-mini")
        val gitRepo = field("Git remote بکاپ", "git_repo")
        val gitUser = field("Git user", "git_user")
        val gitPass = field("Git token", "git_pass", true)
        val driveEmail = field("Drive email", "drive_email")
        val driveFolder = field("پوشه Drive", "drive_folder", def = "NetworkEncyclopedia-Backup")
        val save = Button(this).apply {
            text = "ذخیره همه"
            setOnClickListener {
                prefs.edit()
                    .putString("host", host.text.toString().trim())
                    .putString("token", token.text.toString())
                    .putBoolean("auto_sync", autoSync.isChecked)
                    .putString("ai_provider", aiProvider.text.toString().trim())
                    .putString("ai_base", aiBase.text.toString().trim())
                    .putString("ai_api_key", aiKey.text.toString().trim())
                    .putString("ai_model", aiModel.text.toString().trim())
                    .putString("git_repo", gitRepo.text.toString().trim())
                    .putString("git_user", gitUser.text.toString().trim())
                    .putString("git_pass", gitPass.text.toString().trim())
                    .putString("drive_email", driveEmail.text.toString().trim())
                    .putString("drive_folder", driveFolder.text.toString().trim())
                    .apply()
                Toast.makeText(this@SettingsActivity, "ذخیره شد", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
        fun section(t: String) = TextView(this).apply {
            text = t; textSize = 16f; setPadding(0, 18, 0, 6); setTextColor(0xFF60A5FA.toInt())
        }
        val inner = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL; setPadding(28, 28, 28, 28)
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            addView(TextView(this@SettingsActivity).apply { text = "تنظیمات · AI · بکاپ"; textSize = 20f })
            addView(section("ویندوز")); addView(host); addView(token); addView(autoSync)
            addView(section("هوش مصنوعی")); addView(aiProvider); addView(aiBase); addView(aiKey); addView(aiModel)
            addView(section("بکاپ Git")); addView(gitRepo); addView(gitUser); addView(gitPass)
            addView(section("Drive")); addView(driveEmail); addView(driveFolder)
            addView(save)
            addView(Button(this@SettingsActivity).apply {
                text = "منابع معتبر"
                setOnClickListener { startActivity(Intent(this@SettingsActivity, SourcesActivity::class.java)) }
            })
        }
        setContentView(ScrollView(this).apply { addView(inner) })
    }
}
