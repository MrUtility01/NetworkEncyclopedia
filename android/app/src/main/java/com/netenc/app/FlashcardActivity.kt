package com.netenc.app

import android.graphics.Color
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

/** کارت یادگیری: جلو عنوان/خلاصه — پشت متن؛ دکمه‌های مطالعه */
class FlashcardActivity : AppCompatActivity() {
    private lateinit var study: StudyRepository
    private var queue: MutableList<LessonEntity> = mutableListOf()
    private var index = 0
    private var showBack = false

    private lateinit var title: TextView
    private lateinit var body: TextView
    private lateinit var meta: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        study = StudyRepository(this)

        title = TextView(this).apply {
            textSize = 18f
            setTextColor(Color.WHITE)
            setPadding(24, 20, 24, 8)
        }
        meta = TextView(this).apply {
            textSize = 12f
            setTextColor(Color.parseColor("#9AA8BC"))
            setPadding(24, 0, 24, 8)
        }
        body = TextView(this).apply {
            textSize = 14f
            setTextColor(Color.parseColor("#D5DEEA"))
            setPadding(24, 12, 24, 12)
            setTextIsSelectable(true)
        }

        val flip = Button(this).apply {
            text = "برگرداندن کارت (خلاصه ↔ متن)"
            setOnClickListener {
                showBack = !showBack
                render()
            }
        }
        val studied = Button(this).apply {
            text = "✓ مطالعه کردم"
            setOnClickListener { mark("studied") }
        }
        val again = Button(this).apply {
            text = "⏰ دوباره یادآوری کن (۱ ساعت)"
            setOnClickListener { mark("again") }
        }
        val forgot = Button(this).apply {
            text = "✗ بلد نیستم"
            setOnClickListener { mark("forgot") }
        }
        val next = Button(this).apply {
            text = "کارت بعدی بدون ثبت"
            setOnClickListener {
                if (queue.isNotEmpty()) {
                    index = (index + 1) % queue.size
                    showBack = false
                    render()
                }
            }
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Color.parseColor("#0F1419"))
            addView(title)
            addView(meta)
            addView(flip)
            addView(studied)
            addView(again)
            addView(forgot)
            addView(next)
            addView(ScrollView(this@FlashcardActivity).apply { addView(body) },
                LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))
        }
        setContentView(root)

        lifecycleScope.launch { loadQueue() }
    }

    private suspend fun loadQueue() {
        val dao = AppDatabase.get(this).lessonDao()
        val due = withContext(Dispatchers.IO) { study.dueNow(30) }
        val lessons = if (due.isNotEmpty()) {
            due.mapNotNull { withContext(Dispatchers.IO) { dao.byUid(it.lessonUid) } }
        } else {
            // دروس نخونده / تصادفی از بانک
            withContext(Dispatchers.IO) { dao.allActive().shuffled().take(40) }
        }
        queue = lessons.toMutableList()
        index = 0
        showBack = false
        if (queue.isEmpty()) {
            title.text = "کارتی نیست"
            body.text = "ابتدا فهرست درختی را باز کنید تا بانک پر شود."
        } else render()
    }

    private fun render() {
        if (queue.isEmpty()) return
        val e = queue[index]
        title.text = e.titleFa
        meta.text = "${index + 1}/${queue.size} · ${e.chapterTitle} · ${e.tags}"
        body.text = if (showBack) {
            buildString {
                appendLine(e.fullContent.take(4000))
                if (e.commands.isNotBlank()) {
                    appendLine("\n—— دستورات (نمونه) ——")
                    appendLine(e.commands.take(2000))
                }
            }
        } else {
            e.summary.ifBlank { "(خلاصه خالی — کارت را برگردانید)" }
        }
    }

    private fun mark(action: String) {
        if (queue.isEmpty()) return
        val e = queue[index]
        lifecycleScope.launch {
            val row = withContext(Dispatchers.IO) { study.mark(e.uid, action) }
            Toast.makeText(
                this@FlashcardActivity,
                "${row.status} · مرور بعد: ${row.intervalHours}h",
                Toast.LENGTH_SHORT
            ).show()
            queue.removeAt(index)
            if (queue.isEmpty()) {
                title.text = "تمام شد برای الان"
                body.text = "بعداً با یادآوری ساعتی برمی‌گردیم."
            } else {
                if (index >= queue.size) index = 0
                showBack = false
                render()
            }
        }
    }
}
