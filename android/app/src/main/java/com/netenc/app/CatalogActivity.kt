package com.netenc.app

import android.content.Intent
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.ListView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/** فهرست با مسیر کامل: فصل › گروه › درس */
class CatalogActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val title = TextView(this).apply {
            text = "فهرست آفلاین"
            textSize = 18f
            setPadding(32, 32, 32, 16)
            typeface = Ui.persianTypeface()
        }
        val list = ListView(this)
        val root = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Ui.BG)
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
            title.text = "فهرست — ${items.size} درس · محتوا $filled · ${items.map { it.chapterOrder }.toSet().size} فصل"
            val labels = items.map { e ->
                val flag = if (e.fullContent.length > 80) "✓" else "○"
                val ch = e.chapterTitle.ifBlank { "فصل ${e.chapterOrder}" }
                val sub = e.subTitle.ifBlank { "عمومی" }
                val les = e.titleFa.ifBlank { e.uid }
                "$flag $ch\n    › $sub\n    › $les"
            }
            list.adapter = ArrayAdapter(
                this@CatalogActivity,
                android.R.layout.simple_list_item_1,
                labels
            )
            list.setOnItemClickListener { _, _, pos, _ ->
                startActivity(
                    Intent(this@CatalogActivity, LessonDetailActivity::class.java)
                        .putExtra("uid", items[pos].uid)
                )
            }
        }
    }
}
