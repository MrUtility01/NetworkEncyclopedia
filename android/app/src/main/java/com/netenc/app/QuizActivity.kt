package com.netenc.app

import android.graphics.Color
import android.graphics.drawable.GradientDrawable
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
import kotlin.random.Random

class QuizActivity : AppCompatActivity() {
    private lateinit var study: StudyRepository
    private lateinit var qView: TextView
    private lateinit var scoreView: TextView
    private val optionBtns = mutableListOf<Button>()
    private var pool: List<LessonEntity> = emptyList()
    private var current: LessonEntity? = null
    private var correctIdx = 0
    private var score = 0
    private var total = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        study = StudyRepository(this)
        scoreView = TextView(this).apply {
            textSize = 15f
            setTextColor(Color.WHITE)
            typeface = Ui.persianTypeface()
            setPadding(16, 14, 16, 14)
            background = GradientDrawable().apply {
                cornerRadius = 14f
                setColor(Color.parseColor("#1D4ED8"))
            }
        }
        qView = TextView(this).apply {
            textSize = 16f
            setTextColor(Ui.TEXT)
            typeface = Ui.persianTypeface()
            setPadding(16, 18, 16, 18)
            setBackgroundColor(Ui.CARD)
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Ui.BG)
            setPadding(20, 20, 20, 20)
            addView(TextView(this@QuizActivity).apply {
                text = "آزمون چهارگزینه‌ای"
                textSize = 20f
                setTextColor(Ui.TEXT)
                typeface = Ui.persianTypeface()
            })
            addView(scoreView)
            addView(qView)
            repeat(4) { i ->
                val b = Button(this@QuizActivity).apply {
                    text = "گزینه ${i + 1}"
                    typeface = Ui.persianTypeface()
                    setTextColor(Ui.TEXT)
                    setBackgroundColor(Ui.CARD)
                    setOnClickListener { onPick(i) }
                }
                optionBtns.add(b)
                addView(b)
            }
            addView(Button(this@QuizActivity).apply {
                text = "سؤال بعدی"
                typeface = Ui.persianTypeface()
                setTextColor(Color.WHITE)
                setBackgroundColor(Ui.ACCENT)
                setOnClickListener { nextQuestion() }
            })
        }
        setContentView(ScrollView(this).apply {
            setBackgroundColor(Ui.BG)
            addView(root)
        })
        lifecycleScope.launch {
            pool = withContext(Dispatchers.IO) {
                AppDatabase.get(this@QuizActivity).lessonDao().allActive()
                    .filter { it.titleFa.isNotBlank() }.shuffled().take(200)
            }
            if (pool.size < 4) qView.text = "بانک درس کافی نیست — بازسازی محتوا را بزنید."
            else nextQuestion()
        }
    }

    private fun nextQuestion() {
        if (pool.size < 4) return
        val answer = pool.random()
        current = answer
        correctIdx = Random.nextInt(4)
        val distractors = pool.filter { it.uid != answer.uid }.shuffled().take(3)
        val options = MutableList(4) { LessonEntity(uid = "", titleFa = "?") }
        options[correctIdx] = answer
        var d = 0
        for (i in 0..3) {
            if (i == correctIdx) continue
            options[i] = distractors[d++]
        }
        val styles = listOf(
            "کدام موضوع با این توضیح هم‌خوان است؟\n\n«${answer.summary.take(180).ifBlank { answer.titleFa }}»",
            "دستورات زیر مربوط به کدام درس است؟\n\n${answer.commands.lines().filter { it.isNotBlank() && !it.startsWith(\"#\") }.take(3).joinToString(\"\\n\").ifBlank { answer.titleFa }}",
            "در فصل «${answer.chapterTitle}» کدام عنوان درست است؟"
        )
        qView.text = styles.random()
        optionBtns.forEachIndexed { i, btn ->
            btn.isEnabled = true
            btn.setTextColor(Ui.TEXT)
            btn.setBackgroundColor(Ui.CARD)
            btn.text = options[i].titleFa.take(80)
        }
        scoreView.text = "امتیاز $score / $total  ·  Active Recall"
    }

    private fun onPick(i: Int) {
        val cur = current ?: return
        total++
        optionBtns.forEach { it.isEnabled = false }
        if (i == correctIdx) {
            score++
            optionBtns[i].setBackgroundColor(Color.parseColor("#166534"))
            optionBtns[i].setTextColor(Color.WHITE)
            Toast.makeText(this, "درست ✓", Toast.LENGTH_SHORT).show()
            lifecycleScope.launch { withContext(Dispatchers.IO) { study.mark(cur.uid, "good") } }
        } else {
            optionBtns[i].setBackgroundColor(Color.parseColor("#B91C1C"))
            optionBtns[i].setTextColor(Color.WHITE)
            optionBtns[correctIdx].setBackgroundColor(Color.parseColor("#166534"))
            optionBtns[correctIdx].setTextColor(Color.WHITE)
            Toast.makeText(this, "نادرست — گزینه درست مشخص شد", Toast.LENGTH_SHORT).show()
            lifecycleScope.launch { withContext(Dispatchers.IO) { study.mark(cur.uid, "again") } }
        }
        scoreView.text = "امتیاز $score / $total"
    }
}
