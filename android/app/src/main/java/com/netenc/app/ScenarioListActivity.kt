package com.netenc.app

import android.content.Intent
import android.graphics.Color
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

class ScenarioListActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val title = TextView(this).apply {
            text = "سناریوهای Capstone سازمانی"
            textSize = 18f
            setTextColor(Color.WHITE)
            setPadding(28, 24, 28, 12)
            setBackgroundColor(Color.parseColor("#1A2332"))
        }
        val list = ListView(this)
        val root = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Color.parseColor("#0F1419"))
            addView(title)
            addView(list, android.widget.LinearLayout.LayoutParams(
                android.widget.LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f
            ))
        }
        setContentView(root)

        lifecycleScope.launch {
            val items = withContext(Dispatchers.IO) {
                AppDatabase.get(this@ScenarioListActivity).scenarioDao().all()
            }
            title.text = "Capstone — ${items.size} سناریو"
            list.adapter = ArrayAdapter(
                this@ScenarioListActivity,
                android.R.layout.simple_list_item_2,
                android.R.id.text1,
                items.map { "${it.code}\n${it.titleFa} · ${it.users} کاربر · ${it.sites} سایت" }
            )
            list.setOnItemClickListener { _, _, pos, _ ->
                startActivity(
                    Intent(this@ScenarioListActivity, ScenarioDetailActivity::class.java)
                        .putExtra("code", items[pos].code)
                )
            }
        }
    }
}
