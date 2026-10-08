package com.netenc.app

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
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
    private lateinit var body: TextView
    private lateinit var study: StudyRepository
    private var currentTab = 0
    private val tabButtons = mutableListOf<Button>()

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
        val tabNames = listOf("خلاصه", "متن", "دستورات", "آزمایشگاه", "نکات")
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

        body = Ui.text(this, "", 14.5f, Ui.TEXT).apply {
            setPadding(24, 20, 24, 32)
            setLineSpacing(0f, 1.25f)
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

        val btnCopy = Button(this).apply {
            text = "کپی تب فعلی"
            typeface = Ui.persianTypeface()
            setOnClickListener {
                val cm = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                cm.setPrimaryClip(ClipData.newPlainText("netenc", tabText()))
                Toast.makeText(this@LessonDetailActivity, "کپی شد", Toast.LENGTH_SHORT).show()
            }
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Ui.BG)
            addView(title)
            addView(meta)
            addView(studyRow)
            addView(tabs)
            addView(btnCopy)
            addView(
                ScrollView(this@LessonDetailActivity).apply { addView(body) },
                LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f)
            )
        }
        setContentView(root)

        lifecycleScope.launch {
            val e = withContext(Dispatchers.IO) {
                AppDatabase.get(this@LessonDetailActivity).lessonDao().byUid(uid)
            } ?: return@launch
            lesson = e
            title.text = e.titleFa
            meta.text = listOfNotNull(e.chapterTitle, e.subTitle, e.tags).filter { it.isNotBlank() }.joinToString(" · ")
            renderTab()
        }
    }

    private fun tabText(): String {
        val e = lesson ?: return ""
        return when (currentTab) {
            0 -> e.summary.ifBlank { "خلاصه برای این درس خالی است." }
            1 -> e.fullContent.ifBlank { "متن کامل خالی است. از منوی اصلی بازسازی محتوا را بزنید." }
            2 -> e.commands.ifBlank { "دستوراتی ثبت نشده." }
            3 -> {
                val lab = e.examples.ifBlank { e.notes }
                if (lab.isBlank()) {
                    "آزمایشگاه هنوز برای این درس پر نشده.\n1) متن را بخوانید\n2) دستورات را اجرا کنید\n3) نتیجه را یادداشت کنید"
                } else lab
            }
            else -> e.notes.ifBlank { "نکته‌ای ثبت نشده." }
        }
    }

    private fun renderTab() {
        body.text = tabText()
        body.typeface = Ui.persianTypeface()
        body.textDirection = View.TEXT_DIRECTION_RTL
    }
}
