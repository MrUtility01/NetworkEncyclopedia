package com.netenc.app

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.LessonRepository
import com.netenc.app.data.OfflineSeeder
import com.netenc.app.sync.SyncClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.time.Instant

class MainActivity : AppCompatActivity() {
    private lateinit var hostInput: EditText
    private lateinit var tokenInput: EditText
    private lateinit var logView: TextView
    private lateinit var repo: LessonRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        repo = LessonRepository(this)
        hostInput = findViewById(R.id.hostInput)
        tokenInput = findViewById(R.id.tokenInput)
        logView = findViewById(R.id.logView)

        val prefs = getSharedPreferences("netenc", MODE_PRIVATE)
        hostInput.setText(prefs.getString("host", ""))
        tokenInput.setText(prefs.getString("token", ""))

        findViewById<Button>(R.id.btnCatalog).setOnClickListener {
            startActivity(Intent(this, CatalogActivity::class.java))
        }
        findViewById<Button>(R.id.btnHello).setOnClickListener { hello() }
        findViewById<Button>(R.id.btnSync).setOnClickListener { sync() }
        findViewById<Button>(R.id.btnOpenWeb).setOnClickListener {
            val h = hostInput.text.toString().trim()
            if (h.isBlank()) {
                log("اول IP ویندوز را وارد کنید (فقط برای وب اختیاری)")
            } else {
                startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(h)))
            }
        }

        // seed آفلاین — بدون سرور
        lifecycleScope.launch {
            log("بارگذاری فهرست آفلاین…")
            try {
                val n = withContext(Dispatchers.IO) { OfflineSeeder.ensureSeeded(this@MainActivity) }
                val last = withContext(Dispatchers.IO) { repo.getLastSync() }
                log("✓ آفلاین آماده: $n درس در Room")
                log("آخرین sync اختیاری: ${last.ifBlank { "هرگز" }}")
                log("بدون ویندوز هم می‌توانید «فهرست آفلاین» را باز کنید.")
            } catch (e: Exception) {
                log("seed: ${e.message}")
            }
        }
    }

    private fun savePrefs() {
        getSharedPreferences("netenc", MODE_PRIVATE).edit()
            .putString("host", hostInput.text.toString().trim())
            .putString("token", tokenInput.text.toString())
            .apply()
    }

    private fun client(): SyncClient {
        savePrefs()
        return SyncClient(
            baseUrl = hostInput.text.toString().trim(),
            token = tokenInput.text.toString().trim(),
            deviceId = android.provider.Settings.Secure.getString(
                contentResolver, android.provider.Settings.Secure.ANDROID_ID
            ) ?: "android"
        )
    }

    private fun log(msg: String) {
        logView.append("\n$msg")
    }

    private fun hello() {
        val h = hostInput.text.toString().trim()
        if (h.isBlank()) {
            log("برای اتصال اختیاری، IP ویندوز لازم است. برای مطالعه آفلاین به فهرست بروید.")
            return
        }
        lifecycleScope.launch {
            log("— اتصال اختیاری…")
            try {
                val body = withContext(Dispatchers.IO) { client().hello() }
                log(body)
            } catch (e: Exception) {
                log("سرور در دسترس نیست (طبیعی اگر ویندوز خاموش است): ${e.message}")
            }
        }
    }

    private fun sync() {
        val h = hostInput.text.toString().trim()
        if (h.isBlank()) {
            log("همگام‌سازی اختیاری است — IP ویندوز را فقط وقتی می‌خواهید sync کنید وارد کنید.")
            return
        }
        lifecycleScope.launch {
            log("— همگام‌سازی اختیاری…")
            try {
                val c = client()
                val since = withContext(Dispatchers.IO) { repo.getLastSync() }.ifBlank { null }
                val manifest = withContext(Dispatchers.IO) { c.manifest(since) }
                log("manifest: ${manifest.items.size}")
                var pulled = 0
                for (chunk in manifest.items.map { it.uid }.chunked(100)) {
                    val body = withContext(Dispatchers.IO) { c.pull(chunk) }
                    pulled += withContext(Dispatchers.IO) { repo.upsertFromPullJson(body) }
                }
                log("pull: $pulled")
                val pushArr = withContext(Dispatchers.IO) { repo.buildPushArray() }
                if (pushArr.length() > 0) {
                    log("push: " + withContext(Dispatchers.IO) { c.push(pushArr) })
                }
                withContext(Dispatchers.IO) { repo.setLastSync(Instant.now().toString()) }
                log("✓ sync تمام — محلی: " + withContext(Dispatchers.IO) { repo.count() })
            } catch (e: Exception) {
                log("sync ناموفق (اپ همچنان آفلاین کار می‌کند): ${e.message}")
            }
        }
    }
}
