package com.netenc.app

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.ListView
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
import com.netenc.app.data.LessonEntity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/** مرور آفلاین درس‌ها از SQLite (Room) */
class CatalogActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val title = TextView(this).apply {
            text = "فهرست آفلاین"
            textSize = 18f
            setPadding(32, 32, 32, 16)
        }
        val list = ListView(this)
        val root = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            addView(title)
            addView(
                list,
                android.widget.LinearLayout.LayoutParams(
                    android.widget.LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f
                )
            )
        }
        setContentView(root)

        lifecycleScope.launch {
            val items = withContext(Dispatchers.IO) {
                AppDatabase.get(this@CatalogActivity).lessonDao().allActive()
            }
            val filled = items.count { it.fullContent.length > 80 }
            title.text = "فهرست آفلاین — ${items.size} درس (محتوا: $filled)"
            val labels = items.map { e ->
                val flag = if (e.fullContent.length > 80) "✓" else "○"
                "$flag ${e.titleFa.ifBlank { e.uid }}"
            }
            list.adapter = ArrayAdapter(
                this@CatalogActivity,
                android.R.layout.simple_list_item_1,
                labels
            )
            list.setOnItemClickListener { _, _, pos, _ ->
                showLesson(items[pos])
            }
        }
    }

    private fun showLesson(e: LessonEntity) {
        val body = buildString {
            appendLine(e.titleFa)
            appendLine()
            appendLine("—— خلاصه / دیدگاه کلی ——")
            appendLine(e.summary.ifBlank { "(خلاصه خالی)" })
            appendLine()
            appendLine("—— متن درس ——")
            appendLine(e.fullContent.ifBlank { "(متن خالی — یک‌بار اپ را پاک و دوباره نصب کنید)" })
            if (e.commands.isNotBlank()) {
                appendLine()
                appendLine("—— دستورات ——")
                appendLine(e.commands)
            }
            if (e.examples.isNotBlank()) {
                appendLine()
                appendLine("—— مثال ——")
                appendLine(e.examples)
            }
            if (e.notes.isNotBlank()) {
                appendLine()
                appendLine("—— نکات ——")
                appendLine(e.notes)
            }
        }
        AlertDialog.Builder(this)
            .setTitle(e.titleFa.take(48))
            .setMessage(body)
            .setPositiveButton("بستن", null)
            .show()
    }
}
