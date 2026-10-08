package com.netenc.app

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.os.Bundle
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val uid = intent.getStringExtra("uid") ?: return finish()
        study = StudyRepository(this)

        val title = TextView(this).apply {
            textSize = 16f
            setPadding(20, 16, 20, 8)
            setTextColor(0xFFFFFFFF.toInt())
        }
        val meta = TextView(this).apply {
            textSize = 12f
            setPadding(20, 0, 20, 8)
            setTextColor(0xFF9AA8BC.toInt())
        }
        val tabs = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        val tabNames = listOf("خلاصه", "متن", "دستورات", "Lab", "نکات")
        val tabButtons = mutableListOf<Button>()
        tabNames.forEachIndexed { idx, name ->
            val b = Button(this).apply {
                text = name
                textSize = 11f
                setOnClickListener {
                    currentTab = idx
                    renderTab()
                    tabButtons.forEachIndexed { i, btn -> btn.alpha = if (i == currentTab) 1f else 0.55f }
                }
            }
            tabButtons.add(b)
            tabs.addView(b, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))
        }
        tabButtons[0].alpha = 1f

        body = TextView(this).apply {
            textSize = 14f
            setTextIsSelectable(true)
            setPadding(20, 16, 20, 24)
            setTextColor(0xFFD5DEEA.toInt())
        }

        val studyRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        fun studyBtn(label: String, action: String) = Button(this).apply {
            text = label
            textSize = 11f
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
            setOnClickListener {
                val cm = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                cm.setPrimaryClip(ClipData.newPlainText("netenc", tabText()))
                Toast.makeText(this@LessonDetailActivity, "کپی شد", Toast.LENGTH_SHORT).show()
            }
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(0xFF0F1419.toInt())
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
            0 -> e.summary.ifBlank { "(خلاصه خالی)" }
            1 -> e.fullContent.ifBlank { "(متن خالی)" }
            2 -> e.commands.ifBlank { "(دستورات خالی)" }
            3 -> e.examples.ifBlank {
                e.notes.ifBlank { "(Lab خالی — بازسازی محتوا)" }
            }
            else -> e.notes.ifBlank { "(نکته‌ای ثبت نشده)" }
        }
    }

    private fun renderTab() {
        body.text = tabText()
    }
}
