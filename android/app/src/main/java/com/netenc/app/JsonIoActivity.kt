package com.netenc.app

import android.os.Bundle
import android.os.Environment
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
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

/** خروجی و ورودی JSON — معادل export/import ویندوز */
class JsonIoActivity : AppCompatActivity() {
    private lateinit var log: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        log = TextView(this).apply {
            textSize = 13f
            setTextIsSelectable(true)
            setPadding(16, 16, 16, 16)
        }
        val exportBtn = Button(this).apply {
            text = "خروجی JSON (دروس + سناریو)"
            setOnClickListener { exportJson() }
        }
        val importBtn = Button(this).apply {
            text = "ورودی JSON از فایل export"
            setOnClickListener { importJson() }
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setPadding(20, 20, 20, 20)
            addView(TextView(this@JsonIoActivity).apply {
                text = "ورود / خروج JSON"
                textSize = 18f
                setPadding(0, 0, 0, 12)
            })
            addView(exportBtn)
            addView(importBtn)
            addView(ScrollView(this@JsonIoActivity).apply { addView(log) },
                LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))
        }
        setContentView(root)
        log.text = "مسیر پیش‌فرض:\nDownload/NetEnc_export.json"
    }

    private fun exportFile(): File {
        val dir = getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS) ?: filesDir
        return File(dir, "NetEnc_export.json")
    }

    private fun exportJson() {
        lifecycleScope.launch {
            try {
                val db = AppDatabase.get(this@JsonIoActivity)
                val lessons = withContext(Dispatchers.IO) { db.lessonDao().allActive() }
                val scenarios = withContext(Dispatchers.IO) { db.scenarioDao().all() }
                val root = JSONObject()
                root.put("app", "EngineerJokar-NetEnc")
                root.put("version", 1)
                val arr = JSONArray()
                for (e in lessons) {
                    arr.put(JSONObject().apply {
                        put("uid", e.uid)
                        put("title_fa", e.titleFa)
                        put("summary", e.summary)
                        put("full_content", e.fullContent)
                        put("commands", e.commands)
                        put("examples", e.examples)
                        put("notes", e.notes)
                        put("chapter", e.chapterTitle)
                        put("sub", e.subTitle)
                        put("level", e.tags)
                    })
                }
                root.put("lessons", arr)
                val scArr = JSONArray()
                for (s in scenarios) {
                    scArr.put(JSONObject().apply {
                        put("code", s.code)
                        put("title_fa", s.titleFa)
                        put("business_context", s.businessContext)
                        put("tasks", s.tasks)
                        put("expected_result", s.expectedResult)
                    })
                }
                root.put("scenarios", scArr)
                val f = exportFile()
                withContext(Dispatchers.IO) { f.writeText(root.toString()) }
                log.text = "خروجی ذخیره شد:\n${f.absolutePath}\n\nدروس: ${lessons.size}\nسناریو: ${scenarios.size}"
                Toast.makeText(this@JsonIoActivity, "Export OK", Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                log.text = "خطا: ${e.message}"
            }
        }
    }

    private fun importJson() {
        lifecycleScope.launch {
            try {
                val f = exportFile()
                if (!f.exists()) {
                    log.text = "فایل نیست:\n${f.absolutePath}"
                    return@launch
                }
                val text = withContext(Dispatchers.IO) { f.readText() }
                val root = JSONObject(text)
                val arr = root.optJSONArray("lessons") ?: JSONArray()
                val dao = AppDatabase.get(this@JsonIoActivity).lessonDao()
                val batch = mutableListOf<com.netenc.app.data.LessonEntity>()
                for (i in 0 until arr.length()) {
                    val o = arr.getJSONObject(i)
                    val uid = o.optString("uid")
                    if (uid.isBlank()) continue
                    val old = withContext(Dispatchers.IO) { dao.byUid(uid) }
                    batch.add(
                        (old ?: com.netenc.app.data.LessonEntity(uid = uid)).copy(
                            titleFa = o.optString("title_fa", old?.titleFa ?: ""),
                            summary = o.optString("summary", old?.summary ?: ""),
                            fullContent = o.optString("full_content", old?.fullContent ?: ""),
                            commands = o.optString("commands", old?.commands ?: ""),
                            examples = o.optString("examples", old?.examples ?: ""),
                            notes = o.optString("notes", old?.notes ?: ""),
                            contentHash = "json-import",
                            lastUpdated = java.time.Instant.now().toString()
                        )
                    )
                    if (batch.size >= 100) {
                        withContext(Dispatchers.IO) { dao.upsertAll(batch.toList()) }
                        batch.clear()
                    }
                }
                if (batch.isNotEmpty()) withContext(Dispatchers.IO) { dao.upsertAll(batch) }
                log.text = "Import انجام شد — ${arr.length()} رکورد از\n${f.absolutePath}"
            } catch (e: Exception) {
                log.text = "خطا import: ${e.message}"
            }
        }
    }
}
