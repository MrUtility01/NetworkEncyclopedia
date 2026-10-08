package com.netenc.app

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

class SourcesActivity : AppCompatActivity() {
    private lateinit var listBox: LinearLayout
    private val items = mutableListOf<JSONObject>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        listBox = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(8, 8, 8, 8)
        }
        val scroll = ScrollView(this).apply { addView(listBox) }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(20, 20, 20, 20)
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            addView(TextView(this@SourcesActivity).apply {
                text = "منابع معتبر (قابل ویرایش)"
                textSize = 20f
                setPadding(0, 0, 0, 12)
            })
            addView(TextView(this@SourcesActivity).apply {
                text = "لیست سایت‌ها و مستندات رسمی. می‌توانید لینک کم/زیاد کنید."
                textSize = 13f
                setPadding(0, 0, 0, 12)
            })
            addView(Button(this@SourcesActivity).apply {
                text = "افزودن منبع"
                setOnClickListener { addDialog() }
            })
            addView(Button(this@SourcesActivity).apply {
                text = "بازنشانی به پیش‌فرض"
                setOnClickListener {
                    userFile().delete()
                    load()
                    Toast.makeText(this@SourcesActivity, "بازنشانی شد", Toast.LENGTH_SHORT).show()
                }
            })
            addView(scroll)
        }
        setContentView(root)
        load()
    }

    private fun userFile() = File(filesDir, "sources_user.json")

    private fun load() {
        items.clear()
        listBox.removeAllViews()
        val raw = when {
            userFile().exists() -> userFile().readText(Charsets.UTF_8)
            else -> try {
                assets.open("sources.json").bufferedReader(Charsets.UTF_8).readText()
            } catch (_: Exception) { "[]" }
        }
        try {
            val arr = JSONArray(raw)
            for (i in 0 until arr.length()) items.add(arr.getJSONObject(i))
        } catch (_: Exception) {}
        render()
    }

    private fun render() {
        listBox.removeAllViews()
        for ((idx, obj) in items.withIndex()) {
            val title = obj.optString("title")
            val url = obj.optString("url")
            val note = obj.optString("note")
            val cat = obj.optString("category")
            val row = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                setPadding(12, 12, 12, 12)
                setBackgroundColor(0x22FFFFFF)
            }
            row.addView(TextView(this).apply { text = "$title  [$cat]"; textSize = 15f })
            row.addView(TextView(this).apply { text = note; textSize = 12f })
            row.addView(TextView(this).apply {
                text = url; textSize = 11f; setTextColor(0xFF64B5F6.toInt())
            })
            val actions = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
            actions.addView(Button(this).apply {
                text = "بازکردن"
                setOnClickListener {
                    try { startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) }
                    catch (e: Exception) { Toast.makeText(this@SourcesActivity, e.message, Toast.LENGTH_SHORT).show() }
                }
            })
            actions.addView(Button(this).apply {
                text = "حذف"
                setOnClickListener { items.removeAt(idx); save(); render() }
            })
            row.addView(actions)
            listBox.addView(row)
            listBox.addView(TextView(this).apply { text = " "; textSize = 6f })
        }
    }

    private fun save() {
        val arr = JSONArray()
        items.forEach { arr.put(it) }
        userFile().writeText(arr.toString(2), Charsets.UTF_8)
    }

    private fun addDialog() {
        val title = EditText(this).apply { hint = "عنوان" }
        val url = EditText(this).apply {
            hint = "https://..."
            layoutDirection = android.view.View.LAYOUT_DIRECTION_LTR
        }
        val note = EditText(this).apply { hint = "توضیح کوتاه" }
        val box = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(24, 16, 24, 8)
            addView(title); addView(url); addView(note)
        }
        AlertDialog.Builder(this)
            .setTitle("منبع جدید")
            .setView(box)
            .setPositiveButton("افزودن") { _, _ ->
                val t = title.text.toString().trim()
                val u = url.text.toString().trim()
                if (t.isBlank() || u.isBlank()) {
                    Toast.makeText(this, "عنوان و URL لازم است", Toast.LENGTH_SHORT).show()
                    return@setPositiveButton
                }
                items.add(JSONObject().apply {
                    put("id", "user-${System.currentTimeMillis()}")
                    put("title", t); put("url", u); put("category", "User")
                    put("note", note.text.toString().trim()); put("enabled", true)
                })
                save(); render()
            }
            .setNegativeButton("لغو", null)
            .show()
    }
}
