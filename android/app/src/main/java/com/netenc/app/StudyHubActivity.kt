package com.netenc.app

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.StudyRepository
import com.netenc.app.reminder.ReminderScheduler
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class StudyHubActivity : AppCompatActivity() {
    private lateinit var study: StudyRepository
    private lateinit var statsView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        study = StudyRepository(this)
        statsView = TextView(this).apply {
            textSize = 14f
            setTextColor(Color.parseColor("#D5DEEA"))
            setPadding(8, 8, 8, 16)
        }
        val goalInput = EditText(this).apply {
            hint = "هدف روزانه (تعداد کارت)"
            setText(study.dailyGoal().toString())
            inputType = android.text.InputType.TYPE_CLASS_NUMBER
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Color.parseColor("#0F1419"))
            setPadding(24, 24, 24, 24)
            addView(TextView(this@StudyHubActivity).apply {
                text = "مرکز یادگیری عمیق"
                textSize = 20f
                setTextColor(Color.WHITE)
                setPadding(0, 0, 0, 12)
            })
            addView(statsView)
            addView(goalInput)
            addView(Button(this@StudyHubActivity).apply {
                text = "ذخیره هدف روزانه"
                setOnClickListener {
                    val n = goalInput.text.toString().toIntOrNull() ?: 15
                    study.setDailyGoal(n)
                    Toast.makeText(this@StudyHubActivity, "هدف: $n کارت", Toast.LENGTH_SHORT).show()
                    refresh()
                }
            })
            addView(section("مرور فاصله‌دار (SRS)"))
            addView(btn("🃏 مرور مفهوم (خلاصه ↔ متن)") {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "review"))
            })
            addView(btn("⌨️ حدس دستور (Active Recall)") {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "command"))
            })
            addView(btn("🔧 سناریوی عیب‌یابی") {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "trouble"))
            })
            addView(section("آزمون و مسیر"))
            addView(btn("📝 آزمون چهارگزینه‌ای") {
                startActivity(Intent(this@StudyHubActivity, QuizActivity::class.java))
            })
            addView(btn("📚 فهرست درختی") {
                startActivity(Intent(this@StudyHubActivity, TreeCatalogActivity::class.java))
            })
            addView(btn("🎯 Capstone / سناریو") {
                startActivity(Intent(this@StudyHubActivity, ScenarioListActivity::class.java))
            })
            addView(section("یادآوری"))
            addView(btn("یادآوری هر ۱ ساعت") {
                ReminderScheduler.scheduleHourly(this@StudyHubActivity)
                Toast.makeText(this@StudyHubActivity, "فعال شد", Toast.LENGTH_SHORT).show()
            })
            addView(btn("یادآوری هر ۳۰ دقیقه") {
                ReminderScheduler.scheduleMinutes(this@StudyHubActivity, 30)
                Toast.makeText(this@StudyHubActivity, "۳۰ دقیقه فعال شد", Toast.LENGTH_SHORT).show()
            })
            addView(TextView(this@StudyHubActivity).apply {
                setTextColor(Color.parseColor("#9AA8BC"))
                textSize = 12f
                setPadding(0, 16, 0, 0)
                text = "روزانه: ۱۵ کارت due + ۵ آزمون + یک سناریو + یک درس جدید"
            })
        }
        setContentView(ScrollView(this).apply { addView(root) })
        refresh()
    }

    override fun onResume() { super.onResume(); refresh() }

    private fun refresh() {
        lifecycleScope.launch {
            val st = withContext(Dispatchers.IO) { study.stats() }
            statsView.text = buildString {
                appendLine("📊 امروز: ${st["today"]} / ${st["goal"]} کارت")
                appendLine("🔥 زنجیره: ${st["streak"]} روز")
                appendLine("⏰ due: ${st["due"]} · learning: ${st["learning"]} · known: ${st["known"]}")
                if ((st["today"] ?: 0) >= (st["goal"] ?: 15)) appendLine("\n🎯 هدف امروز محقق شد!")
            }
        }
    }

    private fun section(t: String) = TextView(this).apply {
        text = t; textSize = 15f; setTextColor(Color.parseColor("#93C5FD")); setPadding(0, 16, 0, 8)
    }

    private fun btn(label: String, onClick: () -> Unit) = Button(this).apply {
        text = label; setOnClickListener { onClick() }
    }
}
