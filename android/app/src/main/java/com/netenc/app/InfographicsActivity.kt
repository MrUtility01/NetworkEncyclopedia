package com.netenc.app

import android.graphics.Color
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.webkit.WebView
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject

/**
 * Offline SVG gallery. The asset is exported from server/core/infographics.py
 * during APK builds, so Android and Windows share the same canonical diagrams.
 */
class InfographicsActivity : AppCompatActivity() {
    private data class Diagram(val title: String, val svg: String)

    private lateinit var searchInput: EditText
    private lateinit var statusView: TextView
    private lateinit var webView: WebView
    private var diagrams: List<Diagram> = emptyList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Ui.BG)
            setPadding(18, 16, 18, 12)
        }
        root.addView(TextView(this).apply {
            text = "دیاگرام‌ها و اینفوگرافیک شبکه"
            textSize = 21f
            setTextColor(Ui.TEXT)
            typeface = Ui.persianTypeface()
            setPadding(0, 0, 0, 8)
        })
        root.addView(TextView(this).apply {
            text = "نمایش آفلاین · جستجو بر اساس نام مفهوم، پروتکل یا ابزار"
            textSize = 12f
            setTextColor(Ui.MUTED)
            typeface = Ui.persianTypeface()
            setPadding(0, 0, 0, 8)
        })

        searchInput = EditText(this).apply {
            hint = "مثلاً OSPF، VLAN، DNS، VPN…"
            setSingleLine(true)
            textSize = 14f
            setTextColor(Ui.TEXT)
            setHintTextColor(Ui.MUTED)
            typeface = Ui.persianTypeface()
            setPadding(14, 10, 14, 10)
            setBackgroundColor(Color.WHITE)
        }
        root.addView(searchInput, LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ))

        statusView = TextView(this).apply {
            text = "در حال بارگذاری نمودارها…"
            textSize = 12f
            setTextColor(Ui.MUTED)
            typeface = Ui.persianTypeface()
            setPadding(0, 8, 0, 8)
        }
        root.addView(statusView)

        webView = WebView(this).apply {
            setBackgroundColor(Color.parseColor("#F4F6F9"))
            settings.javaScriptEnabled = false
            settings.domStorageEnabled = false
            settings.allowFileAccess = false
            settings.allowContentAccess = false
            isVerticalScrollBarEnabled = true
            isHorizontalScrollBarEnabled = false
        }
        root.addView(webView, LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f
        ))
        setContentView(root)

        searchInput.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                render(s?.toString().orEmpty())
            }
            override fun afterTextChanged(s: Editable?) = Unit
        })

        lifecycleScope.launch {
            diagrams = withContext(Dispatchers.IO) { readDiagrams() }
            statusView.text = "${diagrams.size} نمودار آماده است"
            render(searchInput.text?.toString().orEmpty())
        }
    }

    private fun readDiagrams(): List<Diagram> {
        return try {
            val raw = assets.open("infographics.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
            val root = JSONObject(raw)
            val array = root.optJSONArray("items") ?: return fallbackDiagrams()
            val out = ArrayList<Diagram>(array.length())
            for (i in 0 until array.length()) {
                val row = array.optJSONObject(i) ?: continue
                val title = row.optString("title").trim()
                val svg = row.optString("svg").trim()
                if (title.isNotEmpty() && svg.contains("<svg", ignoreCase = true) &&
                    svg.contains("</svg>", ignoreCase = true)) {
                    out.add(Diagram(title, svg))
                }
            }
            out.ifEmpty { fallbackDiagrams() }
        } catch (_: Exception) {
            fallbackDiagrams()
        }
    }

    private fun fallbackDiagrams(): List<Diagram> {
        val source = listOf(
            "مسیر پکت تا اینترنت" to listOf("PC", "Switch", "Router", "Firewall", "ISP"),
            "TCP Three-way Handshake" to listOf("Client", "SYN", "SYN-ACK", "ACK"),
            "DHCP DORA" to listOf("Discover", "Offer", "Request", "ACK"),
            "DNS Resolution" to listOf("Client", "Resolver", "Root", "Authoritative"),
            "OSPF Neighbor" to listOf("Down", "Init", "2-Way", "Full")
        )
        return source.map { (title, labels) ->
            val bw = 96
            val gap = if (labels.size > 1) 14 else 0
            val total = labels.size * bw + (labels.size - 1) * gap
            val start = ((680 - total) / 2).coerceAtLeast(8)
            val boxes = labels.mapIndexed { index, label ->
                val x = start + index * (bw + gap)
                """<rect x="$x" y="65" width="$bw" height="42" rx="8" fill="#dbeafe" stroke="#2563eb"/><text x="${x + bw / 2}" y="90" text-anchor="middle" font-size="11" fill="#0f172a">${escapeHtml(label)}</text>"""
            }.joinToString("")
            Diagram(title, """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 135" width="100%"><text x="16" y="25" font-size="14" fill="#0f172a">${escapeHtml(title)}</text>$boxes</svg>""")
        }
    }

    private fun render(query: String) {
        if (!::webView.isInitialized || diagrams.isEmpty()) return
        val q = query.trim()
        val filtered = if (q.isBlank()) diagrams else diagrams.filter { it.title.contains(q, ignoreCase = true) }
        statusView.text = if (q.isBlank()) {
            "${diagrams.size} نمودار آماده است"
        } else {
            "${filtered.size} نتیجه برای «$q»"
        }
        val cards = filtered.joinToString("\n") { item ->
            """<article class="card"><h2>${escapeHtml(item.title)}</h2><div class="diagram">${sanitizeSvg(item.svg)}</div></article>"""
        }
        val empty = if (filtered.isEmpty()) """<p class="empty">نموداری با این عبارت پیدا نشد.</p>""" else ""
        val html = """
            <!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <style>
              body{margin:0;padding:4px;background:#f4f6f9;color:#0f172a;font-family:Tahoma,sans-serif;line-height:1.65}
              .card{background:#fff;border:1px solid #dbe3ef;border-radius:14px;margin:10px 0;padding:12px;box-shadow:0 2px 5px #0f172a0a}
              h2{font-size:15px;margin:0 0 8px;font-weight:700}
              .diagram{overflow-x:auto}
              svg{display:block;width:100%;height:auto;max-width:100%;min-width:300px}
              .empty{padding:18px;text-align:center;color:#64748b;background:#fff;border-radius:12px}
            </style></head><body>$cards$empty</body></html>
        """.trimIndent()
        webView.loadDataWithBaseURL(null, html, "text/html", "UTF-8", null)
    }

    private fun sanitizeSvg(svg: String): String {
        return svg
            .replace(Regex("""(?is)<script\b.*?</script\s*>"""), "")
            .replace(Regex("""(?i)\s+on[a-z]+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)"""), "")
    }

    private fun escapeHtml(value: String): String = value
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
        .replace("'", "&#39;")
}
