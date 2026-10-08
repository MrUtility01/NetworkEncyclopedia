package com.netenc.app

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.sync.SyncClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray

class MainActivity : AppCompatActivity() {
    private lateinit var hostInput: EditText
    private lateinit var tokenInput: EditText
    private lateinit var logView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        hostInput = findViewById(R.id.hostInput)
        tokenInput = findViewById(R.id.tokenInput)
        logView = findViewById(R.id.logView)

        val prefs = getSharedPreferences("netenc", MODE_PRIVATE)
        hostInput.setText(prefs.getString("host", "http://192.168.1.10:5050"))
        tokenInput.setText(prefs.getString("token", ""))

        findViewById<Button>(R.id.btnHello).setOnClickListener { hello() }
        findViewById<Button>(R.id.btnSync).setOnClickListener { sync() }
        findViewById<Button>(R.id.btnOpenWeb).setOnClickListener {
            val url = hostInput.text.toString().trim()
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
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
        lifecycleScope.launch {
            log("— اتصال…")
            try {
                val body = withContext(Dispatchers.IO) { client().hello() }
                log(body)
            } catch (e: Exception) {
                log("خطا: ${e.message}")
            }
        }
    }

    private fun sync() {
        lifecycleScope.launch {
            log("— همگام‌سازی…")
            try {
                val c = client()
                val manifest = withContext(Dispatchers.IO) { c.manifest() }
                log("manifest: ${manifest.items.size} رکورد")
                val uids = manifest.items.take(200).map { it.uid }
                if (uids.isNotEmpty()) {
                    val pulled = withContext(Dispatchers.IO) { c.pull(uids) }
                    log("pull bytes: ${pulled.length}")
                }
                // push محلی خالی در اسکلت — بعداً Room DB
                val pushed = withContext(Dispatchers.IO) { c.push(JSONArray()) }
                log("push: $pushed")
                log("✓ همگام‌سازی تمام شد (اسکلت)")
            } catch (e: Exception) {
                log("خطا: ${e.message}")
            }
        }
    }
}
