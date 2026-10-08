package com.netenc.app

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.Editable
import android.text.TextWatcher
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ListView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
import com.netenc.app.data.LessonEntity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class SearchActivity : AppCompatActivity() {
    private lateinit var input: EditText
    private lateinit var title: TextView
    private lateinit var list: ListView
    private var items: List<LessonEntity> = emptyList()
    private val handler = Handler(Looper.getMainLooper())
    private var pending: Runnable? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val initial = intent.getStringExtra("q") ?: ""
        title = TextView(this).apply { text = "جستجوی زنده"; setPadding(24, 16, 24, 8); textSize = 16f }
        input = EditText(this).apply {
            hint = "حداقل ۲ حرف…"; setText(initial); setPadding(24, 12, 24, 12)
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
        }
        list = ListView(this)
        val aiBtn = Button(this).apply { text = "پرسش از AI"; setOnClickListener { askAi() } }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(0xFF0F1419.toInt())
            addView(title); addView(input); addView(aiBtn)
            addView(list, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))
        }
        setContentView(root)
        input.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                pending?.let { handler.removeCallbacks(it) }
                val q = s?.toString()?.trim().orEmpty()
                if (q.length < 2) { title.text = "حداقل ۲ حرف"; return }
                val r = Runnable { doSearch(q) }
                pending = r
                handler.postDelayed(r, 280)
            }
        })
        list.setOnItemClickListener { _, _, pos, _ ->
            if (pos in items.indices) {
                startActivity(Intent(this, LessonDetailActivity::class.java).putExtra("uid", items[pos].uid))
            }
        }
        if (initial.length >= 2) doSearch(initial)
    }

    private fun doSearch(q: String) {
        lifecycleScope.launch {
            items = withContext(Dispatchers.IO) {
                AppDatabase.get(this@SearchActivity).lessonDao().search(q).take(80)
            }
            title.text = "${items.size} نتیجه برای «$q»"
            list.adapter = ArrayAdapter(this@SearchActivity, android.R.layout.simple_list_item_1,
                items.map { "${it.chapterTitle} › ${it.titleFa}" })
        }
    }

    private fun askAi() {
        val q = input.text.toString().trim()
        if (q.length < 2) { Toast.makeText(this, "سوال را بنویسید", Toast.LENGTH_SHORT).show(); return }
        val prefs = getSharedPreferences("netenc", MODE_PRIVATE)
        val key = prefs.getString("ai_api_key", "") ?: ""
        if (key.isBlank()) {
            Toast.makeText(this, "کلید AI در تنظیمات خالی است", Toast.LENGTH_LONG).show()
            startActivity(Intent(this, SettingsActivity::class.java)); return
        }
        val base = (prefs.getString("ai_base", "https://api.openai.com/v1") ?: "").trimEnd('/')
        val model = prefs.getString("ai_model", "gpt-4o-mini") ?: "gpt-4o-mini"
        title.text = "AI…"
        lifecycleScope.launch {
            try {
                val localCtx = withContext(Dispatchers.IO) {
                    AppDatabase.get(this@SearchActivity).lessonDao().search(q).take(5)
                        .joinToString("\n") { "- ${it.titleFa}: ${it.summary.take(120)}" }
                }
                val prompt = "دستیار شبکه Engineer Jokar.\nسوال: $q\nزمینه:\n$localCtx\nپاسخ: مفهوم، دستورات، عیب‌یابی، امنیت — فارسی فنی."
                val answer = withContext(Dispatchers.IO) { callChat(base, key, model, prompt) }
                title.text = "پاسخ AI"
                list.adapter = ArrayAdapter(this@SearchActivity, android.R.layout.simple_list_item_1, listOf(answer))
                items = emptyList()
            } catch (e: Exception) {
                title.text = "خطا: ${e.message}"
                Toast.makeText(this@SearchActivity, e.message, Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun callChat(base: String, key: String, model: String, prompt: String): String {
        val url = URL("$base/chat/completions")
        val conn = (url.openConnection() as HttpURLConnection).apply {
            requestMethod = "POST"
            setRequestProperty("Authorization", "Bearer $key")
            setRequestProperty("Content-Type", "application/json")
            doOutput = true; connectTimeout = 30000; readTimeout = 90000
        }
        val body = JSONObject().put("model", model)
            .put("messages", JSONArray()
                .put(JSONObject().put("role", "system").put("content", "Senior network engineer tutor."))
                .put(JSONObject().put("role", "user").put("content", prompt)))
            .put("temperature", 0.3)
        OutputStreamWriter(conn.outputStream, Charsets.UTF_8).use { it.write(body.toString()) }
        val code = conn.responseCode
        val text = (if (code in 200..299) conn.inputStream else conn.errorStream).bufferedReader().readText()
        if (code !in 200..299) throw RuntimeException("HTTP $code: ${text.take(300)}")
        return JSONObject(text).getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content")
    }
}
