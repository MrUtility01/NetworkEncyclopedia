package com.netenc.app

import android.graphics.Color
import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
import com.netenc.app.data.LessonEntity
import com.netenc.app.data.StudyRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class FlashcardActivity : AppCompatActivity() {
    private lateinit var study: StudyRepository
    private var queue: MutableList<LessonEntity> = mutableListOf()
    private var index = 0
    private var showBack = false
    private var mode = "review"
    private var sessionDone = 0
    private lateinit var title: TextView
    private lateinit var body: TextView
    private lateinit var meta: TextView
    private lateinit var progress: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        study = StudyRepository(this)
        mode = intent.getStringExtra("mode") ?: "review"
        title = TextView(this).apply { textSize = 18f; setTextColor(Ui.TEXT); typeface = Ui.persianTypeface(); setPadding(24, 20, 24, 8) }
        progress = TextView(this).apply { textSize = 12f; setTextColor(Ui.ACCENT); typeface = Ui.persianTypeface(); setPadding(24, 0, 24, 4) }
        meta = TextView(this).apply { textSize = 12f; setTextColor(Ui.MUTED); typeface = Ui.persianTypeface(); setPadding(24, 0, 24, 8) }
        body = TextView(this).apply { textSize = 14f; setTextColor(Ui.TEXT); typeface = Ui.persianTypeface(); setPadding(24, 12, 24, 12); setTextIsSelectable(true); setBackgroundColor(Ui.CARD) }

        val modeBtn = Button(this).apply {
            text = "حالت: ${modeLabel()} (تغییر)"
            setTextColor(Color.WHITE); setBackgroundColor(Ui.ACCENT); typeface = Ui.persianTypeface()
            setOnClickListener {
                mode = when (mode) { "review" -> "command"; "command" -> "trouble"; else -> "review" }
                text = "حالت: ${modeLabel()} (تغییر)"; showBack = false; render()
            }
        }
        val flip = Button(this).apply {
            text = "برگرداندن کارت / نمایش پاسخ"
            setTextColor(Color.WHITE); setBackgroundColor(Color.parseColor("#334155")); typeface = Ui.persianTypeface()
            setOnClickListener { showBack = !showBack; render() }
        }
        val again = Button(this).apply { text = "Again · بلد نیستم (۱س)"; setTextColor(Color.WHITE); setBackgroundColor(Color.parseColor("#B91C1C")); typeface = Ui.persianTypeface(); setOnClickListener { mark("again") } }
        val hard = Button(this).apply { text = "Hard · سخت"; setTextColor(Color.WHITE); setBackgroundColor(Color.parseColor("#C2410C")); typeface = Ui.persianTypeface(); setOnClickListener { mark("hard") } }
        val good = Button(this).apply { text = "Good · بلدم"; setTextColor(Color.WHITE); setBackgroundColor(Color.parseColor("#166534")); typeface = Ui.persianTypeface(); setOnClickListener { mark("good") } }
        val easy = Button(this).apply { text = "Easy · خیلی راحت"; setTextColor(Color.WHITE); setBackgroundColor(Ui.ACCENT); typeface = Ui.persianTypeface(); setOnClickListener { mark("easy") } }
        val skip = Button(this).apply {
            text = "رد کردن بدون ثبت"
            setTextColor(Ui.TEXT); setBackgroundColor(Ui.CARD); typeface = Ui.persianTypeface()
            setOnClickListener { if (queue.isNotEmpty()) { index = (index + 1) % queue.size; showBack = false; render() } }
        }
        val hint = Button(this).apply {
            text = "راهنما / نکته یادگیری"
            setTextColor(Ui.TEXT); setBackgroundColor(Ui.ACCENT_SOFT); typeface = Ui.persianTypeface()
            setOnClickListener { showHint() }
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Ui.BG)
            addView(progress); addView(title); addView(meta); addView(modeBtn); addView(flip); addView(hint)
            addView(again); addView(hard); addView(good); addView(easy); addView(skip)
            addView(ScrollView(this@FlashcardActivity).apply { addView(body) }, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))
        }
        setContentView(root)
        lifecycleScope.launch { loadQueue() }
    }

    private fun modeLabel() = when (mode) { "command" -> "حدس دستور"; "trouble" -> "عیب‌یابی"; else -> "مرور مفهوم" }

    private suspend fun loadQueue() {
        val dao = AppDatabase.get(this).lessonDao()
        val chapterFilter = intent.getStringExtra("chapter")
        val due = withContext(Dispatchers.IO) { study.dueNow(40) }
        var lessons = if (due.isNotEmpty()) due.mapNotNull { withContext(Dispatchers.IO) { dao.byUid(it.lessonUid) } }
        else withContext(Dispatchers.IO) { dao.allActive().filter { it.summary.isNotBlank() || it.fullContent.isNotBlank() }.shuffled().take(50) }
        if (!chapterFilter.isNullOrBlank()) {
            lessons = lessons.filter { it.chapterTitle == chapterFilter }
            if (lessons.isEmpty()) {
                lessons = withContext(Dispatchers.IO) {
                    dao.allActive().filter { it.chapterTitle == chapterFilter }.shuffled().take(40)
                }
            }
        }
        queue = lessons.toMutableList(); index = 0; showBack = false
        if (queue.isEmpty()) { title.text = "کارتی نیست"; body.text = "ابتدا فهرست درختی یا بازسازی محتوا." } else render()
        refreshProgress()
    }

    private fun refreshProgress() {
        progress.text = "جلسه: $sessionDone کارت · صف: ${queue.size} · حالت: ${modeLabel()}"
    }

    private fun render() {
        if (queue.isEmpty()) return
        val L = queue[index % queue.size]
        title.text = L.titleFa
        meta.text = "${L.chapterTitle} · ${L.subTitle} · ${L.tags}"
        body.text = if (!showBack) {
            when (mode) {
                "command" -> "چه دستوری برای «${L.titleFa}»؟\n\n(برگردان برای دیدن دستورات)"
                "trouble" -> "اگر «${L.titleFa}» خراب شود چه علائمی می‌بینی؟\n\n(برگردان برای عیب‌یابی)"
                else -> L.summary.ifBlank { L.titleFa }
            }
        } else {
            buildString {
                append(L.fullContent.take(1200).ifBlank { L.summary })
                if (L.commands.isNotBlank()) append("\n\n— دستورات —\n").append(L.commands.take(600))
                if (L.examples.isNotBlank()) append("\n\n— مثال —\n").append(L.examples.take(400))
            }
        }
        refreshProgress()
    }

    private fun mark(grade: String) {
        if (queue.isEmpty()) return
        val L = queue[index % queue.size]
        lifecycleScope.launch {
            withContext(Dispatchers.IO) { study.mark(L.uid, grade) }
            sessionDone++
            if (grade == "again") {
                // keep in queue near end
            } else if (queue.size > 1) {
                queue.removeAt(index % queue.size)
                if (index >= queue.size) index = 0
            }
            showBack = false
            if (queue.isEmpty()) {
                title.text = "تمام شد"; body.text = "این دور تمام شد. آفرین."
            } else render()
            Toast.makeText(this@FlashcardActivity, grade, Toast.LENGTH_SHORT).show()
        }
    }

    private fun showHint() {
        AlertDialog.Builder(this)
            .setTitle("نکته یادگیری")
            .setMessage("Again = دوباره زود · Hard = سخت · Good = بلدم · Easy = خیلی راحت\nهر علامت، فاصله مرور بعدی (SRS) را تنظیم می‌کند.")
            .setPositiveButton("باشه", null)
            .show()
    }
}
