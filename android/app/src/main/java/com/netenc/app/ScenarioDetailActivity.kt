package com.netenc.app

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ScenarioDetailActivity : AppCompatActivity() {
    private var textAll = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val code = intent.getStringExtra("code") ?: return finish()
        val body = TextView(this).apply {
            setTextIsSelectable(true)
            setTextColor(Color.parseColor("#D5DEEA"))
            textSize = 14f
            setPadding(24, 20, 24, 32)
        }
        val copy = Button(this).apply {
            text = "کپی کل سناریو"
            setOnClickListener {
                val cm = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                cm.setPrimaryClip(ClipData.newPlainText("scenario", textAll))
                Toast.makeText(this@ScenarioDetailActivity, "کپی شد", Toast.LENGTH_SHORT).show()
            }
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Color.parseColor("#0F1419"))
            addView(copy)
            addView(ScrollView(this@ScenarioDetailActivity).apply { addView(body) },
                LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))
        }
        setContentView(root)

        lifecycleScope.launch {
            val s = withContext(Dispatchers.IO) {
                AppDatabase.get(this@ScenarioDetailActivity).scenarioDao().byCode(code)
            } ?: return@launch
            textAll = buildString {
                appendLine(s.code)
                appendLine(s.titleFa)
                appendLine("سطح: ${s.level} · سختی: ${s.difficulty}")
                appendLine("کاربر: ${s.users} · سایت: ${s.sites}")
                appendLine("Vendor: ${s.vendors}")
                appendLine()
                appendLine("=== زمینه کسب‌وکار ===")
                appendLine(s.businessContext)
                appendLine()
                appendLine("=== نیازمندی‌ها ===")
                appendLine(s.requirements)
                appendLine()
                appendLine("=== محدودیت‌ها ===")
                appendLine(s.constraintsText)
                appendLine()
                appendLine("=== حادثه / علائم ===")
                appendLine(s.incident)
                appendLine()
                appendLine("=== مسیر بررسی (Tasks) ===")
                appendLine(s.tasks)
                appendLine()
                appendLine("=== راهنما ===")
                appendLine(s.hints)
                appendLine()
                appendLine("=== نتیجه مورد انتظار ===")
                appendLine(s.expectedResult)
                appendLine()
                appendLine("=== رویکرد حل ===")
                appendLine(s.solution)
                appendLine()
                appendLine("=== Verification ===")
                appendLine(s.verification)
            }
            body.text = textAll
        }
    }
}
