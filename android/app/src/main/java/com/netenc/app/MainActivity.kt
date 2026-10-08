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
import com.netenc.app.data.AppDatabase
import com.netenc.app.data.LessonRepository
import com.netenc.app.data.OfflineSeeder
import com.netenc.app.data.ScenarioSeeder
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
        findViewById<Button>(R.id.btnScenarios).setOnClickListener {
            startActivity(Intent(this, ScenarioListActivity::class.java))
        }
        findViewById<Button>(R.id.btnStats).setOnClickListener { showStats() }
        findViewById<Button>(R.id.btnApi).setOnClickListener {
            startActivity(Intent(this, ApiExplorerActivity::class.java))
        }
        findViewById<Button>(R.id.btnJson).setOnClickListener {
            startActivity(Intent(this, JsonIoActivity::class.java))
        }
        findViewById<Button>(R.id.btnSettings).setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }
        findViewById<Button>(R.id.btnReseed).setOnClickListener { forceReseed() }
        findViewById<Button>(R.id.btnHello).setOnClickListener { hello() }
        findViewById<Button>(R.id.btnSync).setOnClickListener { sync() }
        findViewById<Button>(R.id.btnOpenWeb).setOnClickListener {
            val h = hostInput.text.toString().trim()
            if (h.isBlank()) log("IP را در تنظیمات یا همین‌جا وارد کنید")
            else startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(h)))
        }
        findViewById<Button>(R.id.btnAbout).setOnClickListener {
            AlertDialog.Builder(this)
                .setTitle("Engineer Jokar")
                .setMessage("دایرةالمعارف شبکه\n09132184122\n\nویندوز و اندروید مستقل\nSync اختیاری LAN")
                .setPositiveButton("باشه", null)
                .setNeutralButton("تماس") { _, _ ->
                    startActivity(Intent(Intent.ACTION_DIAL, Uri.parse("tel:09132184122")))
                }
                .show()
        }

        lifecycleScope.launch { seedAll(force = false) }

        if (prefs.getBoolean("auto_sync", false) && !prefs.getString("host", "").isNullOrBlank()) {
            hostInput.postDelayed({ sync() }, 2500)
        }
    }

    private fun forceReseed() {
        lifecycleScope.launch {
            withContext(Dispatchers.IO) {
                val dao = AppDatabase.get(this@MainActivity).lessonDao()
                dao.putMeta(com.netenc.app.data.SyncMetaEntity("offline_seeded_v5", "0"))
                dao.putMeta(com.netenc.app.data.SyncMetaEntity("offline_seeded_v4", "0"))
            }
            seedAll(force = true)
        }
    }

    private suspend fun seedAll(force: Boolean) {
        log(if (force) "بازسازی اجباری…" else "بارگذاری بانک…")
        try {
            val n = withContext(Dispatchers.IO) { OfflineSeeder.ensureSeeded(this@MainActivity) }
            val sc = withContext(Dispatchers.IO) { ScenarioSeeder.ensure(this@MainActivity) }
            val filled = withContext(Dispatchers.IO) {
                AppDatabase.get(this@MainActivity).lessonDao().countFilled()
            }
            log("✓ درس: $n · متن‌دار: $filled · سناریو: $sc")
        } catch (e: Exception) {
            log("seed: ${e.message}")
        }
    }

    private fun showStats() {
        lifecycleScope.launch {
            val db = AppDatabase.get(this@MainActivity)
            val lessons = withContext(Dispatchers.IO) { db.lessonDao().countActive() }
            val filled = withContext(Dispatchers.IO) { db.lessonDao().countFilled() }
            val sc = withContext(Dispatchers.IO) { db.scenarioDao().count() }
            AlertDialog.Builder(this@MainActivity)
                .setTitle("آمار SQLite")
                .setMessage("درس: $lessons\nمتن کامل: $filled\nسناریو: $sc")
                .setPositiveButton("باشه", null)
                .show()
        }
    }

    private fun askSearch() {
        val input = EditText(this).apply { hint = "VLAN / OSPF / AD" }
        AlertDialog.Builder(this)
            .setTitle("جستجو")
            .setView(input)
            .setPositiveButton("برو") { _, _ ->
                val q = input.text.toString().trim()
                if (q.isNotBlank()) startActivity(Intent(this, SearchActivity::class.java).putExtra("q", q))
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
            log("آدرس API را وارد کنید")
            return
        }
        lifecycleScope.launch {
            try {
                log(withContext(Dispatchers.IO) { client().hello() })
            } catch (e: Exception) {
                log("خطا: ${e.message}")
            }
        }
    }

    private fun sync() {
        if (hostInput.text.toString().trim().isBlank()) {
            log("Sync نیاز به IP ویندوز دارد")
            return
        }
        lifecycleScope.launch {
            try {
                val c = client()
                val since = withContext(Dispatchers.IO) { repo.getLastSync() }.ifBlank { null }
                val m = withContext(Dispatchers.IO) { c.manifest(since) }
                var pulled = 0
                for (chunk in m.items.map { it.uid }.chunked(80)) {
                    val body = withContext(Dispatchers.IO) { c.pull(chunk) }
                    pulled += withContext(Dispatchers.IO) { repo.upsertFromPullJson(body) }
                }
                val pushArr = withContext(Dispatchers.IO) { repo.buildPushArray() }
                if (pushArr.length() > 0) withContext(Dispatchers.IO) { c.push(pushArr) }
                withContext(Dispatchers.IO) { repo.setLastSync(Instant.now().toString()) }
                log("✓ sync pull=$pulled")
            } catch (e: Exception) {
                log("sync: ${e.message}")
            }
        }
    }
}
