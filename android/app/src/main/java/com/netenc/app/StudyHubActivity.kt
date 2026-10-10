package com.netenc.app

import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.GradientDrawable
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
    private lateinit var statsRow: LinearLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        study = StudyRepository(this)
        statsRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
        }
        val goalInput = EditText(this).apply {
            hint = "هدف روزانه (تعداد درس)"
            setText(study.dailyGoal().toString())
            inputType = android.text.InputType.TYPE_CLASS_NUMBER
            setTextColor(Ui.TEXT)
            setHintTextColor(Ui.MUTED)
            setBackgroundColor(Ui.CARD)
            setPadding(16, 16, 16, 16)
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Ui.BG)
            setPadding(24, 24, 24, 24)
            addView(TextView(this@StudyHubActivity).apply {
                text = "مرکز یادگیری عمیق"
                textSize = 22f
                setTextColor(Ui.TEXT)
                typeface = Ui.persianTypeface()
                setPadding(0, 0, 0, 12)
            })
            addView(statsRow)
            addView(goalInput)
            addView(btn("ذخیره هدف", Ui.ACCENT) {
                study.setDailyGoal(goalInput.text.toString().toIntOrNull() ?: 15)
                refresh()
            })
            addView(section("شروع هوشمند"))
            addView(btn("انتخاب فصل → کارت از سطح سبک", Ui.ACCENT) { pickChapterForCards() })
            addView(section("مرور SRS"))
            addView(btn("مرور مفهوم", Color.parseColor("#1D4ED8")) {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "review"))
            })
            addView(btn("حدس دستور", Color.parseColor("#0F766E")) {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "command"))
            })
            addView(btn("عیب‌یابی", Color.parseColor("#C2410C")) {
                startActivity(Intent(this@StudyHubActivity, FlashcardActivity::class.java).putExtra("mode", "trouble"))
            })
            addView(section("آزمون و سناریو"))
            addView(btn("آزمون چهارگزینه‌ای", Color.parseColor("#7C3AED")) {
                startActivity(Intent(this@StudyHubActivity, QuizActivity::class.java))
            })
            addView(btn("درخت درس‌ها", Ui.ACCENT) {
                startActivity(Intent(this@StudyHubActivity, TreeCatalogActivity::class.java))
            })
            addView(btn("سناریوهای Capstone", Color.parseColor("#B45309")) {
                startActivity(Intent(this@StudyHubActivity, ScenarioListActivity::class.java))
            })
            addView(section("یادآوری"))
            addView(btn("یادآوری هر ۱ ساعت", Color.parseColor("#334155")) {
                ReminderScheduler.scheduleHourly(this@StudyHubActivity)
                Toast.makeText(this@StudyHubActivity, "یادآوری ساعتی فعال شد", Toast.LENGTH_SHORT).show()
            })
            addView(btn("یادآوری ۳۰ دقیقه", Color.parseColor("#334155")) {
                ReminderScheduler.scheduleMinutes(this@StudyHubActivity, 30)
                Toast.makeText(this@StudyHubActivity, "یادآوری ۳۰د فعال شد", Toast.LENGTH_SHORT).show()
            })
        }
        setContentView(ScrollView(this).apply {
            setBackgroundColor(Ui.BG)
            addView(root)
        })
        refresh()
    }

    override fun onResume() { super.onResume(); refresh() }

    private fun card(label: String, value: String, accent: Int): TextView {
        return TextView(this).apply {
            text = "$label\n$value"
            textSize = 13f
            setTextColor(Color.WHITE)
            typeface = Ui.persianTypeface()
            setPadding(18, 16, 18, 16)
            val bg = GradientDrawable().apply {
                cornerRadius = 16f
                setColor(accent)
            }
            background = bg
            layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f).apply {
                setMargins(6, 8, 6, 12)
            }
        }
    }

    private fun refresh() {
        lifecycleScope.launch {
            val st = withContext(Dispatchers.IO) { study.stats() }
            statsRow.removeAllViews()
            statsRow.addView(card("امروز", "${st[\"today\"]}/${st[\"goal\"]}", Color.parseColor("#1D4ED8")))
            statsRow.addView(card("Due", "${st[\"due\"]}", Color.parseColor("#C2410C")))
            statsRow.addView(card("زنجیره", "${st[\"streak\"]}", Color.parseColor("#0F766E")))
            statsRow.addView(card("بلد", "${st[\"known\"]}", Color.parseColor("#166534")))
        }
    }

    private fun section(t: String) = TextView(this).apply {
        text = t
        textSize = 15f
        setTextColor(Ui.MUTED)
        typeface = Ui.persianTypeface()
        setPadding(0, 18, 0, 8)
    }

    private fun btn(label: String, color: Int, onClick: () -> Unit) = Button(this).apply {
        text = label
        typeface = Ui.persianTypeface()
        setTextColor(Color.WHITE)
        setBackgroundColor(color)
        setOnClickListener { onClick() }
        setPadding(12, 8, 12, 8)
    }

    private fun pickChapterForCards() {
        lifecycleScope.launch {
            val chapters = withContext(Dispatchers.IO) {
                AppDatabase.get(this@StudyHubActivity).lessonDao().allActive()
                    .map { it.chapterTitle }.filter { it.isNotBlank() }.distinct().sorted()
            }
            if (chapters.isEmpty()) {
                Toast.makeText(this@StudyHubActivity, "بانک خالی — اول فهرست درختی یا بازسازی محتوا", Toast.LENGTH_LONG).show()
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
}
