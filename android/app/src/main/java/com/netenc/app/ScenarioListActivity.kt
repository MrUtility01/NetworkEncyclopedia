package com.netenc.app

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ListView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
import com.netenc.app.data.ScenarioEntity
import com.netenc.app.data.ScenarioSeeder
import com.netenc.app.data.SyncMetaEntity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ScenarioListActivity : AppCompatActivity() {
    private lateinit var status: TextView
    private lateinit var list: ListView
    private var items: List<ScenarioEntity> = emptyList()
    private lateinit var adapter: BaseAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val title = Ui.text(this, "سناریوهای Capstone سازمانی", 18f, Color.WHITE).apply {
            setBackgroundColor(Ui.CARD)
            setTextIsSelectable(false)
        }
        status = Ui.text(this, "در حال بارگذاری…", 13f, Ui.MUTED).apply { setTextIsSelectable(false) }
        val reseed = Button(this).apply {
            text = "پر کردن / بازسازی سناریوها"
            typeface = Ui.persianTypeface()
            setOnClickListener { load(force = true) }
        }
        list = ListView(this).apply { setBackgroundColor(Ui.BG) }

        adapter = object : BaseAdapter() {
            override fun getCount() = items.size
            override fun getItem(position: Int) = items[position]
            override fun getItemId(position: Int) = position.toLong()
            override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
                val row = LinearLayout(this@ScenarioListActivity).apply {
                    orientation = LinearLayout.VERTICAL
                    layoutDirection = View.LAYOUT_DIRECTION_RTL
                    setPadding(28, 22, 28, 22)
                    setBackgroundColor(Ui.BG)
                }
                val s = items[position]
                row.addView(Ui.text(this@ScenarioListActivity, "${s.code}  ${s.titleFa}", 15f, Ui.TEXT).apply {
                    setTextIsSelectable(false)
                })
                row.addView(
                    Ui.text(
                        this@ScenarioListActivity,
                        "${s.users} کاربر · ${s.sites} سایت · ${s.vendors}",
                        12f, Ui.MUTED
                    ).apply { setTextIsSelectable(false) }
                )
                return row
            }
        }
        list.adapter = adapter
        list.setOnItemClickListener { _, _, pos, _ ->
            if (pos in items.indices) {
                startActivity(
                    Intent(this, ScenarioDetailActivity::class.java).putExtra("code", items[pos].code)
                )
            }
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Ui.BG)
            addView(title)
            addView(status)
            addView(reseed)
            addView(list, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))
        }
        setContentView(root)
        load(force = false)
    }

    private fun load(force: Boolean) {
        status.text = "در حال آماده‌سازی سناریوها…"
        lifecycleScope.launch {
            try {
                items = withContext(Dispatchers.IO) {
                    val db = AppDatabase.get(this@ScenarioListActivity)
                    if (force || db.scenarioDao().count() == 0) {
                        db.lessonDao().putMeta(SyncMetaEntity("scenarios_seeded_v4", "0"))
                    }
                    ScenarioSeeder.ensure(this@ScenarioListActivity)
                    db.scenarioDao().all()
                }
                adapter.notifyDataSetChanged()
                if (items.isEmpty()) {
                    status.setTextColor(Color.parseColor("#F87171"))
                    status.text = "خالی است — دکمه بازسازی را بزنید"
                } else {
                    status.setTextColor(Ui.MUTED)
                    status.text = "${items.size} سناریو آماده · یکی را لمس کنید"
                }
            } catch (e: Exception) {
                status.text = "خطا: ${e.message}"
                status.setTextColor(Color.parseColor("#F87171"))
                Toast.makeText(this@ScenarioListActivity, e.message, Toast.LENGTH_LONG).show()
            }
        }
    }
}
