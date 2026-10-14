package com.netenc.app

import android.annotation.SuppressLint
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.webkit.WebView
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
import com.netenc.app.data.LessonEntity
import com.netenc.app.data.StudyRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class LessonDetailActivity : AppCompatActivity() {
    private var lesson: LessonEntity? = null
    private lateinit var web: WebView
    private lateinit var study: StudyRepository
    private var currentTab = 0
    private val tabButtons = mutableListOf<Button>()

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val uid = intent.getStringExtra("uid") ?: return finish()
        study = StudyRepository(this)

        val title = Ui.text(this, "…", 17f, Color.WHITE).apply { setTextIsSelectable(false) }
        val meta = Ui.text(this, "", 12f, Ui.MUTED).apply { setTextIsSelectable(false) }

        val tabs = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutDirection = View.LAYOUT_DIRECTION_RTL
        }
        val tabNames = listOf("خلاصه", "متن+نمودار", "دستورات", "آزمایشگاه", "نکات")
        tabNames.forEachIndexed { idx, name ->
            val b = Button(this).apply {
                text = name
                textSize = 11f
                typeface = Ui.persianTypeface()
                alpha = if (idx == 0) 1f else 0.55f
                setOnClickListener {
                    currentTab = idx
                    renderTab()
                    tabButtons.forEachIndexed { i, btn -> btn.alpha = if (i == currentTab) 1f else 0.55f }
                }
            }
            tabButtons.add(b)
            tabs.addView(b, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))
        }

        web = WebView(this).apply {
            setBackgroundColor(Color.parseColor("#F4F6F9"))
            settings.javaScriptEnabled = false
            settings.defaultTextEncodingName = "utf-8"
        }

        val studyRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        fun studyBtn(label: String, action: String) = Button(this).apply {
            text = label
            textSize = 11f
            typeface = Ui.persianTypeface()
            setOnClickListener {
                val e = lesson ?: return@setOnClickListener
                lifecycleScope.launch {
                    val row = withContext(Dispatchers.IO) { study.mark(e.uid, action) }
                    Toast.makeText(this@LessonDetailActivity, "${row.status} · ${row.intervalHours}h", Toast.LENGTH_SHORT).show()
                }
            }
        }
        studyRow.addView(studyBtn("✓ بلدم", "studied"), LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))
        studyRow.addView(studyBtn("⏰ دوباره", "again"), LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))
        studyRow.addView(studyBtn("✗ بلد نیستم", "forgot"), LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))

        val extraRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        extraRow.addView(Button(this).apply {
            text = "کپی"
            textSize = 11f
            typeface = Ui.persianTypeface()
            setOnClickListener {
                val cm = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                cm.setPrimaryClip(ClipData.newPlainText("netenc", tabText()))
                Toast.makeText(this@LessonDetailActivity, "کپی شد", Toast.LENGTH_SHORT).show()
            }
        }, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))
        extraRow.addView(Button(this).apply {
            text = "کارها"
            textSize = 11f
            typeface = Ui.persianTypeface()
            setOnClickListener {
                startActivity(Intent(this@LessonDetailActivity, WorkspaceActivity::class.java).putExtra("mode", "tasks"))
            }
        }, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))
        extraRow.addView(Button(this).apply {
            text = "یادداشت"
            textSize = 11f
            typeface = Ui.persianTypeface()
            setOnClickListener {
                startActivity(Intent(this@LessonDetailActivity, WorkspaceActivity::class.java).putExtra("mode", "notes"))
            }
        }, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Ui.BG)
            addView(title)
            addView(meta)
            addView(studyRow)
            addView(extraRow)
            addView(tabs)
            addView(web, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))
        }
        setContentView(root)

        lifecycleScope.launch {
            val e = withContext(Dispatchers.IO) {
                AppDatabase.get(this@LessonDetailActivity).lessonDao().byUid(uid)
            } ?: return@launch
            lesson = e
            title.text = e.titleFa
            meta.text = listOf(
                e.chapterTitle.ifBlank { "فصل ${e.chapterOrder}" },
                e.subTitle.ifBlank { "گروه عمومی" },
                e.tags.ifBlank { "L?" }
            ).joinToString("  ›  ")
            renderTab()
        }
    }

    private fun tabText(): String {
        val e = lesson ?: return ""
        return when (currentTab) {
            0 -> e.summary.ifBlank { "خلاصه برای این درس خالی است." }
            1 -> e.fullContent.ifBlank { "متن کامل خالی است. از منوی اصلی «بازسازی» را بزنید." }
            2 -> e.commands.ifBlank { "دستوراتی ثبت نشده." }
            3 -> {
                val lab = e.examples.ifBlank { e.notes }
                if (lab.isBlank()) {
                    "آزمایشگاه خالی است.\n1) متن را بخوانید\n2) دستورات را اجرا کنید\n3) در یادداشت نتیجه را بنویسید"
                } else lab
            }
            else -> e.notes.ifBlank { "نکته‌ای ثبت نشده. از دکمه یادداشت برای ذخیره نکته شخصی استفاده کنید." }
        }
    }

    private fun escapeHtml(s: String): String =
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    private fun toHtml(raw: String): String {
        val parts = mutableListOf<String>()
        var i = 0
        val text = raw
        val lower = text.lowercase()
        while (i < text.length) {
            val start = lower.indexOf("<svg", i)
            if (start < 0) {
                parts.add("<pre style=\"white-space:pre-wrap;font-family:sans-serif;direction:rtl\">" +
                    escapeHtml(text.substring(i)) + "</pre>")
                break
            }
            if (start > i) {
                parts.add("<pre style=\"white-space:pre-wrap;font-family:sans-serif;direction:rtl\">" +
                    escapeHtml(text.substring(i, start)) + "</pre>")
            }
            val end = lower.indexOf("</svg>", start)
            if (end < 0) {
                parts.add("<pre style=\"white-space:pre-wrap;font-family:sans-serif;direction:rtl\">" +
                    escapeHtml(text.substring(start)) + "</pre>")
                break
            }
            parts.add("<div style=\"margin:12px 0;overflow:auto\">" + text.substring(start, end + 6) + "</div>")
            i = end + 6
        }
        return """
            <html><head><meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width,initial-scale=1"/>
            <style>
              body{margin:12px;background:#F4F6F9;color:#0f172a;direction:rtl;font-size:15px;line-height:1.55}
              pre{background:#fff;padding:12px;border-radius:10px;border:1px solid #e2e8f0}
              svg{max-width:100%;height:auto}
            </style></head><body>${parts.joinToString("")}</body></html>
        """.trimIndent()
    }

    private fun renderTab() {
        web.loadDataWithBaseURL(null, toHtml(tabText()), "text/html", "utf-8", null)
    }
}
