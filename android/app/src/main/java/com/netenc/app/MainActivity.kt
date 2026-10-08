package com.netenc.app

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.sync.LocalStore
import com.netenc.app.sync.SyncClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject

class MainActivity : AppCompatActivity() {
    private lateinit var hostInput: EditText
    private lateinit var tokenInput: EditText
    private lateinit var logView: TextView
    private lateinit var store: LocalStore

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        store = LocalStore(this)
        hostInput = findViewById(R.id.hostInput)
        tokenInput = findViewById(R.id.tokenInput)
        logView = findViewById(R.id.logView)
        val prefs = getSharedPreferences("netenc", MODE_PRIVATE)
        hostInput.setText(prefs.getString("host", "http://192.168.1.10:5050"))
        tokenInput.setText(prefs.getString("token", ""))
        findViewById<Button>(R.id.btnHello).setOnClickListener { hello() }
        findViewById<Button>(R.id.btnSync).setOnClickListener { sync() }
        findViewById<Button>(R.id.btnOpenWeb).setOnClickListener {
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(hostInput.text.toString().trim())))
        }
        log("ذخیره محلی: ${'$'}{store.count()} رکورد | آخرین sync: ${'$'}{store.getLastSync().ifBlank { "—" }}")
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

    private fun log(msg: String) { logView.append("\n$msg") }

    private fun hello() {
        lifecycleScope.launch {
            log("— اتصال…")
            try {
                val body = withContext(Dispatchers.IO) { client().hello() }
                log(body)
            } catch (e: Exception) {
                log("خطا: ${'$'}{e.message}")
            }
        }
    }

    private fun sync() {
        lifecycleScope.launch {
            log("— همگام‌سازی دوطرفه…")
            try {
                val c = client()
                val since = store.getLastSync().ifBlank { null }
                val manifest = withContext(Dispatchers.IO) { c.manifest(since) }
                log("manifest: ${'$'}{manifest.items.size} تغییر")
                val uids = manifest.items.map { it.uid }
                if (uids.isNotEmpty()) {
                    var pulled = 0
                    for (chunk in uids.chunked(100)) {
                        val body = withContext(Dispatchers.IO) { c.pull(chunk) }
                        pulled += store.upsertLessonsFromPull(body)
                    }
                    log("pull اعمال شد: ${'$'}pulled")
                }
                val pushArr = store.buildPushRecords()
                if (pushArr.length() > 0) {
                    val pushResult = withContext(Dispatchers.IO) { c.push(pushArr) }
                    log("push: ${'$'}pushResult")
                } else {
                    log("push: چیزی برای ارسال نبود")
                }
                store.setLastSync(java.time.Instant.now().toString())
                log("✓ تمام — محلی: ${'$'}{store.count()} رکورد")
            } catch (e: Exception) {
                log("خطا: ${'$'}{e.message}")
            }
        }
    }
}
