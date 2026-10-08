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
        title = TextView(this).apply { textSize = 18f; setTextColor(Color.WHITE); setPadding(24, 20, 24, 8) }
        progress = TextView(this).apply { textSize = 12f; setTextColor(Color.parseColor("#60A5FA")); setPadding(24, 0, 24, 4) }
        meta = TextView(this).apply { textSize = 12f; setTextColor(Color.parseColor("#9AA8BC")); setPadding(24, 0, 24, 8) }
        body = TextView(this).apply { textSize = 14f; setTextColor(Color.parseColor("#D5DEEA")); setPadding(24, 12, 24, 12); setTextIsSelectable(true) }

        val modeBtn = Button(this).apply {
            text = "حالت: ${modeLabel()} (تغییر)"
            setOnClickListener {
                mode = when (mode) { "review" -> "command"; "command" -> "trouble"; else -> "review" }
                text = "حالت: ${modeLabel()} (تغییر)"; showBack = false; render()
            }
        }
        val flip = Button(this).apply { text = "برگرداندن کارت / نمایش پاسخ"; setOnClickListener { showBack = !showBack; render() } }
        val again = Button(this).apply { text = "Again · بلد نیستم (۱س)"; setBackgroundColor(Color.parseColor("#7F1D1D")); setOnClickListener { mark("again") } }
        val hard = Button(this).apply { text = "Hard · سخت"; setBackgroundColor(Color.parseColor("#9A3412")); setOnClickListener { mark("hard") } }
        val good = Button(this).apply { text = "Good · بلدم"; setBackgroundColor(Color.parseColor("#14532D")); setOnClickListener { mark("good") } }
        val easy = Button(this).apply { text = "Easy · خیلی راحت"; setBackgroundColor(Color.parseColor("#1E3A8A")); setOnClickListener { mark("easy") } }
        val skip = Button(this).apply {
            text = "رد کردن بدون ثبت"
            setOnClickListener { if (queue.isNotEmpty()) { index = (index + 1) % queue.size; showBack = false; render() } }
        }
        val hint = Button(this).apply { text = "راهنما / نکته یادگیری"; setOnClickListener { showHint() } }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Color.parseColor("#0F1419"))
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
        val due = withContext(Dispatchers.IO) { study.dueNow(40) }
        val lessons = if (due.isNotEmpty()) due.mapNotNull { withContext(Dispatchers.IO) { dao.byUid(it.lessonUid) } }
        else withContext(Dispatchers.IO) { dao.allActive().filter { it.summary.isNotBlank() || it.fullContent.isNotBlank() }.shuffled().take(50) }
        queue = lessons.toMutableList(); index = 0; showBack = false
        if (queue.isEmpty()) { title.text = "کارتی نیست"; body.text = "ابتدا فهرست درختی یا بازسازی محتوا." } else render()
        refreshProgress()
    }

    private fun refreshProgress() {
        lifecycleScope.launch {
            val st = withContext(Dispatchers.IO) { study.stats() }
            progress.text = "امروز ${st["today"]}/${st["goal"]} · زنجیره ${st["streak"]} روز · due=${st["due"]} · جلسه $sessionDone"
        }
    }

    private fun render() {
        if (queue.isEmpty()) return
        val e = queue[index]
        title.text = e.titleFa
        meta.text = "${index + 1}/${queue.size} · ${e.chapterTitle} · ${e.tags} · ${modeLabel()}"
        body.text = when {
            !showBack && mode == "command" -> "❓ چه دستوری برای «${e.titleFa}»؟\n\nسطح: ${e.tags}\nفصل: ${e.chapterTitle}\n\nکارت را برگردانید."
            !showBack && mode == "trouble" -> "🔧 سرویس «${e.titleFa}» قطع است.\n\n۱) Symptom؟\n۲) لایه OSI؟\n۳) چه show/diagnose؟\n\nپاسخ با برگرداندن کارت."
            !showBack -> e.summary.ifBlank { "(خلاصه خالی — برگردانید)" }
            mode == "command" -> "✅ دستورات:\n\n${e.commands.take(3500).ifBlank { e.fullContent.take(2500) }}\n\n${e.notes.take(500)}"
            mode == "trouble" -> "RCA: Symptom→Scope→Evidence→RootCause→Fix→Verify\n\n${e.fullContent.take(3000)}\n\n${e.commands.take(2000)}"
            else -> "${e.fullContent.take(4000)}\n\n—— دستورات ——\n${e.commands.take(2000)}\n\n${e.examples.take(800)}"
        }
    }

    private fun showHint() {
        val tips = when (mode) {
            "command" -> "اول show/status، بعد config؛ همیشه Verify و backup."
            "trouble" -> "از L1 شروع کنید؛ capture در نقطه درست؛ یک فرضیه در هر گام."
            else -> "مفهوم را به سناریوی سازمانی وصل کنید؛ دیاگرام ذهنی بکشید."
        }
        AlertDialog.Builder(this).setTitle("نکته").setMessage(tips).setPositiveButton("باشه", null).show()
    }

    private fun mark(action: String) {
        if (queue.isEmpty()) return
        val e = queue[index]
        lifecycleScope.launch {
            val row = withContext(Dispatchers.IO) { study.mark(e.uid, action) }
            sessionDone++
            val whenTxt = if (row.intervalHours >= 24) String.format("%.1f روز", row.intervalHours / 24.0) else "${row.intervalHours} ساعت"
            Toast.makeText(this@FlashcardActivity, "${row.status} · بعد: $whenTxt", Toast.LENGTH_SHORT).show()
            queue.removeAt(index)
            refreshProgress()
            if (queue.isEmpty()) {
                val st = withContext(Dispatchers.IO) { study.stats() }
                title.text = "جلسه تمام"
                body.text = "کارت‌ها: $sessionDone\nامروز: ${st["today"]}/${st["goal"]}\nزنجیره: ${st["streak"]} روز"
            } else {
                if (index >= queue.size) index = 0
                showBack = false; render()
            }
        }
    }
}
