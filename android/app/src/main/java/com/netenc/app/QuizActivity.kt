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
import org.json.JSONArray
import org.json.JSONObject
import kotlin.random.Random

/**
 * آزمون:
 * 1) اگر meta_json/notes دارای assessment.questions باشد از همان
 * 2) وگرنه از خلاصه/دستور/عنوان درس
 */
class QuizActivity : AppCompatActivity() {
    private lateinit var study: StudyRepository
    private lateinit var qView: TextView
    private lateinit var scoreView: TextView
    private val optionBtns = mutableListOf<Button>()
    private var pool: List<LessonEntity> = emptyList()
    private var bank: List<BankQ> = emptyList()
    private var current: LessonEntity? = null
    private var correctIdx = 0
    private var score = 0
    private var total = 0
    private var modeBank = false

    data class BankQ(
        val prompt: String,
        val options: List<String>,
        val correctIndex: Int,
        val lessonUid: String
    )

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
                text = "آزمون"
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
                    .filter { it.titleFa.isNotBlank() }.shuffled().take(300)
            }
            bank = pool.flatMap { extractBank(it) }.shuffled()
            modeBank = bank.size >= 4
            scoreView.text = if (modeBank) "بانک ارزیابی: ${bank.size} سؤال" else "حالت سریع از خلاصه درس"
            if (pool.size < 4 && bank.size < 4) qView.text = "بانک درس کافی نیست — بازسازی محتوا."
            else nextQuestion()
        }
    }

    private fun extractBank(les: LessonEntity): List<BankQ> {
        val out = mutableListOf<BankQ>()
        for (blob in listOf(les.metaJson, les.notes)) {
            if (blob.isBlank()) continue
            try {
                var jsonStr = blob
                if ("EJ_ASSESSMENT" in blob) {
                    val i = blob.indexOf("EJ_ASSESSMENT")
                    val start = blob.indexOf("{", i)
                    val end = blob.lastIndexOf("}")
                    if (start >= 0 && end > start) jsonStr = blob.substring(start, end + 1)
                }
                val root = JSONObject(jsonStr)
                val assessment = root.optJSONObject("assessment") ?: root
                val questions = assessment.optJSONArray("questions") ?: continue
                val answerKey = assessment.optJSONArray("answer_key")
                for (qi in 0 until questions.length()) {
                    val q = questions.getJSONObject(qi)
                    val prompt = q.optString("prompt", q.optString("text", ""))
                    if (prompt.isBlank()) continue
                    val optsArr = q.optJSONArray("options") ?: continue
                    val options = mutableListOf<String>()
                    for (oi in 0 until optsArr.length()) {
                        val o = optsArr.get(oi)
                        options.add(
                            when (o) {
                                is JSONObject -> o.optString("text", o.optString("label", ""))
                                else -> o.toString()
                            }
                        )
                    }
                    if (options.size < 2) continue
                    var correct = q.optInt("correct_index", -1)
                    if (correct < 0 && answerKey != null) {
                        val id = q.optString("id", qi.toString())
                        for (ai in 0 until answerKey.length()) {
                            val a = answerKey.getJSONObject(ai)
                            if (a.optString("id", "") == id || a.optInt("question_index", -1) == qi) {
                                correct = a.optInt("correct_index", a.optInt("answer", 0))
                                break
                            }
                        }
                    }
                    if (correct < 0) correct = 0
                    while (options.size < 4) options.add("—")
                    out.add(BankQ(prompt, options.take(4), correct.coerceIn(0, 3), les.uid))
                }
            } catch (_: Exception) { }
        }
        return out
    }

    private fun nextQuestion() {
        optionBtns.forEach {
            it.isEnabled = true
            it.setTextColor(Ui.TEXT)
            it.setBackgroundColor(Ui.CARD)
        }
        if (modeBank && bank.isNotEmpty()) {
            val q = bank.random()
            current = pool.find { it.uid == q.lessonUid }
            correctIdx = q.correctIndex.coerceIn(0, 3)
            qView.text = q.prompt
            optionBtns.forEachIndexed { i, btn -> btn.text = q.options.getOrElse(i) { "—" } }
            scoreView.text = "امتیاز $score / $total · بانک ارزیابی"
            return
        }
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
            "دستورات زیر مربوط به کدام درس است؟\n\n${answer.commands.lines().filter { it.isNotBlank() && !it.startsWith("#") }.take(3).joinToString("\n").ifBlank { answer.titleFa }}",
            "در فصل «${answer.chapterTitle}» کدام عنوان درست است؟"
        )
        qView.text = styles.random()
        optionBtns.forEachIndexed { i, btn -> btn.text = options[i].titleFa.take(80) }
        scoreView.text = "امتیاز $score / $total · از خلاصه درس"
    }

    private fun onPick(i: Int) {
        total++
        optionBtns.forEach { it.isEnabled = false }
        if (i == correctIdx) {
            score++
            optionBtns[i].setBackgroundColor(Color.parseColor("#166534"))
            optionBtns[i].setTextColor(Color.WHITE)
            Toast.makeText(this, "درست ✓", Toast.LENGTH_SHORT).show()
            current?.let { cur ->
                lifecycleScope.launch { withContext(Dispatchers.IO) { study.mark(cur.uid, "good") } }
            }
        } else {
            optionBtns[i].setBackgroundColor(Color.parseColor("#B91C1C"))
            optionBtns[i].setTextColor(Color.WHITE)
            optionBtns[correctIdx].setBackgroundColor(Color.parseColor("#166534"))
            optionBtns[correctIdx].setTextColor(Color.WHITE)
            Toast.makeText(this, "نادرست", Toast.LENGTH_SHORT).show()
            current?.let { cur ->
                lifecycleScope.launch { withContext(Dispatchers.IO) { study.mark(cur.uid, "again") } }
            }
        }
        scoreView.text = "امتیاز $score / $total"
    }
}
