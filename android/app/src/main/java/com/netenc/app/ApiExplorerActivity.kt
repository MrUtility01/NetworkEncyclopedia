package com.netenc.app

import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import java.util.concurrent.TimeUnit

/** فراخوانی APIهای ویندوز مثل مرورگر — stats/chapters/scenarios/search */
class ApiExplorerActivity : AppCompatActivity() {
    private lateinit var out: TextView
    private val http = OkHttpClient.Builder()
        .connectTimeout(8, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        out = TextView(this).apply {
            setTextIsSelectable(true)
            textSize = 12f
            setPadding(16, 16, 16, 16)
            typeface = android.graphics.Typeface.MONOSPACE
        }
        val prefs = getSharedPreferences("netenc", MODE_PRIVATE)
        val base = prefs.getString("host", "")?.trim().orEmpty()

        fun call(path: String) {
            if (base.isBlank()) {
                out.text = "ابتدا در تنظیمات آدرس API ویندوز را ذخیره کنید"
                return
            }
            lifecycleScope.launch {
                out.text = "در حال درخواست $path …"
                try {
                    val body = withContext(Dispatchers.IO) {
                        val req = Request.Builder().url(base.trimEnd('/') + path).get().build()
                        http.newCall(req).execute().use { it.body?.string() ?: "" }
                    }
                    out.text = body.take(12000)
                } catch (e: Exception) {
                    out.text = "خطا: ${e.message}"
                }
            }
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setPadding(12, 12, 12, 12)
            addView(TextView(this@ApiExplorerActivity).apply {
                text = "API ویندوز (خودکار)"
                textSize = 18f
            })
            addView(Button(this@ApiExplorerActivity).apply {
                text = "GET /api/stats"; setOnClickListener { call("/api/stats") }
            })
            addView(Button(this@ApiExplorerActivity).apply {
                text = "GET /api/chapters"; setOnClickListener { call("/api/chapters") }
            })
            addView(Button(this@ApiExplorerActivity).apply {
                text = "GET /api/scenarios"; setOnClickListener { call("/api/scenarios") }
            })
            addView(Button(this@ApiExplorerActivity).apply {
                text = "GET /api/search?q=VLAN"; setOnClickListener { call("/api/search?q=VLAN") }
            })
            addView(Button(this@ApiExplorerActivity).apply {
                text = "GET /api/sync/hello"; setOnClickListener { call("/api/sync/hello") }
            })
            addView(ScrollView(this@ApiExplorerActivity).apply { addView(out) },
                LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))
        }
        setContentView(root)
        if (base.isNotBlank()) call("/api/stats")
    }
}
