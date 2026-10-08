package com.netenc.app

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
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

        findViewById<Button>(R.id.btnTree).setOnClickListener {
            startActivity(Intent(this, TreeCatalogActivity::class.java))
        }
        findViewById<Button>(R.id.btnCatalog).setOnClickListener {
            startActivity(Intent(this, CatalogActivity::class.java))
        }
        findViewById<Button>(R.id.btnSearch).setOnClickListener { askSearch() }
        findViewById<Button>(R.id.btnHello).setOnClickListener { hello() }
        findViewById<Button>(R.id.btnSync).setOnClickListener { sync() }
        findViewById<Button>(R.id.btnOpenWeb).setOnClickListener {
            val h = hostInput.text.toString().trim()
            if (h.isBlank()) log("IP ویندوز را وارد کنید")
            else startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(h)))
        }

        lifecycleScope.launch {
            log("بارگذاری SQLite آفلاین…")
            try {
                val n = withContext(Dispatchers.IO) { OfflineSeeder.ensureSeeded(this@MainActivity) }
                val filled = withContext(Dispatchers.IO) {
                    com.netenc.app.data.AppDatabase.get(this@MainActivity).lessonDao().countFilled()
                }
                log("✓ $n درس در بانک · $filled با متن کامل")
                log("فهرست درختی را باز کنید — مثل ویندوز")
            } catch (e: Exception) {
                log("seed: ${e.message}")
            }
        }
    }

    private fun askSearch() {
        val input = EditText(this).apply { hint = "مثلاً VLAN یا OSPF" }
        AlertDialog.Builder(this)
            .setTitle("جستجو")
            .setView(input)
            .setPositiveButton("برو") { _, _ ->
                val q = input.text.toString().trim()
                if (q.isNotBlank()) {
                    startActivity(Intent(this, SearchActivity::class.java).putExtra("q", q))
                }
            }
            .setNegativeButton("لغو", null)
            .show()
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
        if (hostInput.text.toString().trim().isBlank()) {
            log("برای مطالعه آفلاین نیازی به سرور نیست")
            return
        }
        lifecycleScope.launch {
            try {
                log(withContext(Dispatchers.IO) { client().hello() })
            } catch (e: Exception) {
                log("سرور در دسترس نیست: ${e.message}")
            }
        }
    }

    private fun sync() {
        if (hostInput.text.toString().trim().isBlank()) {
            log("Sync اختیاری است — فقط با IP ویندوز")
            return
        }
        lifecycleScope.launch {
            try {
                val c = client()
                val since = withContext(Dispatchers.IO) { repo.getLastSync() }.ifBlank { null }
                val m = withContext(Dispatchers.IO) { c.manifest(since) }
                var pulled = 0
                for (chunk in m.items.map { it.uid }.chunked(100)) {
                    val body = withContext(Dispatchers.IO) { c.pull(chunk) }
                    pulled += withContext(Dispatchers.IO) { repo.upsertFromPullJson(body) }
                }
                val pushArr = withContext(Dispatchers.IO) { repo.buildPushArray() }
                if (pushArr.length() > 0) withContext(Dispatchers.IO) { c.push(pushArr) }
                withContext(Dispatchers.IO) { repo.setLastSync(Instant.now().toString()) }
                log("✓ sync: pull=$pulled · محلی=${withContext(Dispatchers.IO) { repo.count() }}")
            } catch (e: Exception) {
                log("sync ناموفق (آفلاین کار می‌کند): ${e.message}")
            }
        }
    }
}
