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
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
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
            hint = "هدف روزانه"
            setText(study.dailyGoal().toString())
            inputType = android.text.InputType.TYPE_CLASS_NUMBER
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Color.parseColor("#0F1419"))
            setPadding(24, 24, 24, 24)
            addView(TextView(this@StudyHubActivity).apply {
                text = "مرکز یادگیری عمیق"; textSize = 20f; setTextColor(Color.WHITE)
            })
            addView(statsView); addView(goalInput)
            addView(btn("ذخیره هدف") {
                study.setDailyGoal(goalInput.text.toString().toIntOrNull() ?: 15)
                refresh()
            })
            addView(section("شروع هوشمند"))
            addView(btn("📚 انتخاب فصل → کارت از سطح سبک") { pickChapterForCards() })
            addView(section("مرور SRS"))
            addView(btn("🃏 مرور مفهوم") {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "review"))
            })
            addView(btn("⌨️ حدس دستور") {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "command"))
            })
            addView(btn("🔧 عیب‌یابی") {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "trouble"))
            })
            addView(section("آزمون"))
            addView(btn("📝 آزمون") { startActivity(Intent(this@StudyHubActivity, QuizActivity::class.java)) })
            addView(btn("🌳 درخت") { startActivity(Intent(this@StudyHubActivity, TreeCatalogActivity::class.java)) })
            addView(btn("🎯 سناریو") { startActivity(Intent(this@StudyHubActivity, ScenarioListActivity::class.java)) })
            addView(section("یادآوری"))
            addView(btn("یادآوری ۱س") { ReminderScheduler.scheduleHourly(this@StudyHubActivity) })
            addView(btn("یادآوری ۳۰د") { ReminderScheduler.scheduleMinutes(this@StudyHubActivity, 30) })
        }
        setContentView(ScrollView(this).apply { addView(root) })
        refresh()
    }

    override fun onResume() { super.onResume(); refresh() }

    private fun pickChapterForCards() {
        lifecycleScope.launch {
            val chapters = withContext(Dispatchers.IO) {
                AppDatabase.get(this@StudyHubActivity).lessonDao().allActive()
                    .map { it.chapterTitle }.filter { it.isNotBlank() }.distinct().sorted()
            }
            if (chapters.isEmpty()) {
                Toast.makeText(this@StudyHubActivity, "بانک خالی — اول فهرست درختی", Toast.LENGTH_LONG).show()
                return@launch
            }
            val arr = chapters.toTypedArray()
            AlertDialog.Builder(this@StudyHubActivity)
                .setTitle("کدام فصل؟ (از سطح سبک)")
                .setItems(arr) { _, which ->
                    startActivity(
                        Intent(this@StudyHubActivity, FlashcardActivity::class.java)
                            .putExtra("mode", "review")
                            .putExtra("chapter", arr[which])
                            .putExtra("from_easy", true)
                    )
                }
                .setNegativeButton("لغو", null).show()
        }
    }

    private fun refresh() {
        lifecycleScope.launch {
            val st = withContext(Dispatchers.IO) { study.stats() }
            statsView.text = "امروز ${st["today"]}/${st["goal"]} · زنجیره ${st["streak"]} · due=${st["due"]}"
        }
    }

    private fun section(t: String) = TextView(this).apply {
        text = t; textSize = 15f; setTextColor(Color.parseColor("#93C5FD")); setPadding(0, 16, 0, 8)
    }
    private fun btn(label: String, onClick: () -> Unit) = Button(this).apply {
        text = label; setOnClickListener { onClick() }
    }
}
