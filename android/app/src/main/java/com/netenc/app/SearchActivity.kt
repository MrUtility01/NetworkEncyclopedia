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

class SearchActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val q = intent.getStringExtra("q") ?: ""
        val title = TextView(this).apply {
            text = "نتایج: $q"
            setPadding(24, 20, 24, 12)
            textSize = 16f
        }
        val list = ListView(this)
        val root = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            addView(title)
            addView(list, android.widget.LinearLayout.LayoutParams(
                android.widget.LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f
            ))
        }
        setContentView(root)

        lifecycleScope.launch {
            val items = withContext(Dispatchers.IO) {
                AppDatabase.get(this@SearchActivity).lessonDao().search(q)
            }
            title.text = "${items.size} نتیجه برای «$q»"
            list.adapter = ArrayAdapter(
                this@SearchActivity,
                android.R.layout.simple_list_item_1,
                items.map { "${it.chapterTitle} › ${it.titleFa}" }
            )
            list.setOnItemClickListener { _, _, pos, _ ->
                startActivity(
                    Intent(this@SearchActivity, LessonDetailActivity::class.java)
                        .putExtra("uid", items[pos].uid)
                )
            }
        }
    }
}
