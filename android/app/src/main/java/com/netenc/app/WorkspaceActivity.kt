package com.netenc.app

import android.graphics.Color
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
import com.netenc.app.data.NoteEntity
import com.netenc.app.data.TaskEntity
import com.netenc.app.data.VaultEntity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.time.Instant
import java.util.UUID
import android.util.Base64
import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec

class WorkspaceActivity : AppCompatActivity() {
    private val db by lazy { AppDatabase.get(this) }
    private lateinit var listView: LinearLayout
    private var mode = "tasks" // tasks | notes | vault

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mode = intent.getStringExtra("mode") ?: "tasks"
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
            setBackgroundColor(Color.parseColor("#F7F8FA"))
            setPadding(20, 20, 20, 20)
        }
        root.addView(TextView(this).apply {
            text = when (mode) {
                "notes" -> "یادداشت‌ها"
                "vault" -> "مدیریت رمزها"
                else -> "مدیریت کارها"
            }
            textSize = 20f
            setTextColor(Color.parseColor("#0F172A"))
        })
        root.addView(Button(this).apply {
            text = "+ جدید"
            setOnClickListener { addItem() }
        })
        listView = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        root.addView(listView)
        setContentView(ScrollView(this).apply { addView(root) })
        refresh()
    }

    private fun now() = Instant.now().toString()

    private fun refresh() {
        lifecycleScope.launch {
            val rows = withContext(Dispatchers.IO) {
                when (mode) {
                    "notes" -> db.workspaceDao().allNotes().map { Triple(it.uid, it.title, it.body) }
                    "vault" -> db.workspaceDao().allVault().map { Triple(it.uid, it.title, it.username) }
                    else -> db.workspaceDao().allTasks().map {
                        Triple(it.uid, (if (it.done) "✓ " else "○ ") + it.title, it.body)
                    }
                }
            }
            listView.removeAllViews()
            if (rows.isEmpty()) {
                listView.addView(TextView(this@WorkspaceActivity).apply {
                    text = "موردی نیست — دکمه + جدید را بزن"
                    setTextColor(Color.GRAY)
                })
            }
            rows.forEach { (uid, title, sub) ->
                listView.addView(TextView(this@WorkspaceActivity).apply {
                    text = "$title\n$sub"
                    textSize = 15f
                    setPadding(8, 16, 8, 16)
                    setTextColor(Color.parseColor("#1E293B"))
                    setOnClickListener { editItem(uid) }
                    setOnLongClickListener {
                        lifecycleScope.launch {
                            withContext(Dispatchers.IO) {
                                when (mode) {
                                    "notes" -> db.workspaceDao().deleteNote(uid)
                                    "vault" -> db.workspaceDao().deleteVault(uid)
                                    else -> db.workspaceDao().deleteTask(uid)
                                }
                            }
                            refresh()
                        }
                        true
                    }
                })
            }
        }
    }

    private fun addItem() {
        val title = EditText(this).apply { hint = "عنوان" }
        val body = EditText(this).apply { hint = if (mode == "vault") "رمز / توضیحات" else "متن" }
        val user = EditText(this).apply { hint = "نام کاربری (اختیاری)" }
        val box = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            addView(title); addView(body)
            if (mode == "vault") addView(user)
        }
        AlertDialog.Builder(this)
            .setTitle("مورد جدید")
            .setView(box)
            .setPositiveButton("ذخیره") { _, _ ->
                val t = title.text.toString().trim()
                if (t.isEmpty()) return@setPositiveButton
                lifecycleScope.launch {
                    withContext(Dispatchers.IO) {
                        val id = UUID.randomUUID().toString()
                        when (mode) {
                            "notes" -> db.workspaceDao().upsertNote(
                                NoteEntity(id, t, body.text.toString(), lastUpdated = now())
                            )
                            "vault" -> db.workspaceDao().upsertVault(
                                VaultEntity(
                                    id, t, user.text.toString(),
                                    secretEnc = simpleEnc(body.text.toString()),
                                    lastUpdated = now()
                                )
                            )
                            else -> db.workspaceDao().upsertTask(
                                TaskEntity(id, t, body.text.toString(), lastUpdated = now())
                            )
                        }
                    }
                    refresh()
                }
            }
            .setNegativeButton("لغو", null)
            .show()
    }

    private fun editItem(uid: String) {
        if (mode != "tasks") return
        lifecycleScope.launch {
            val task = withContext(Dispatchers.IO) {
                db.workspaceDao().allTasks().find { it.uid == uid }
            } ?: return@launch
            withContext(Dispatchers.IO) {
                db.workspaceDao().upsertTask(task.copy(done = !task.done, lastUpdated = now()))
            }
            refresh()
            Toast.makeText(this@WorkspaceActivity, if (!task.done) "انجام شد" else "باز شد", Toast.LENGTH_SHORT).show()
        }
    }

    /** ساده برای ذخیره محلی؛ برای امنیت سازمانی از Keystore استفاده کنید */
    private fun simpleEnc(plain: String): String {
        return try {
            val key = SecretKeySpec("NetEncJokarKey16".toByteArray(), "AES")
            val c = Cipher.getInstance("AES/ECB/PKCS5Padding")
            c.init(Cipher.ENCRYPT_MODE, key)
            Base64.encodeToString(c.doFinal(plain.toByteArray()), Base64.NO_WRAP)
        } catch (_: Exception) {
            plain
        }
    }
}
