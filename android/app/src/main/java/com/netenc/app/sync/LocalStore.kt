package com.netenc.app.sync

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

/** ذخیره آفلاین ساده قبل از Room — فایل JSON در filesDir */
class LocalStore(private val context: Context) {
    private val dir: File = File(context.filesDir, "sync").also { it.mkdirs() }
    private val lessonsFile = File(dir, "lessons.json")
    private val metaFile = File(dir, "meta.json")

    fun getLastSync(): String {
        if (!metaFile.exists()) return ""
        return try {
            JSONObject(metaFile.readText()).optString("last_sync", "")
        } catch (_: Exception) { "" }
    }

    fun setLastSync(iso: String) {
        val o = if (metaFile.exists()) JSONObject(metaFile.readText()) else JSONObject()
        o.put("last_sync", iso)
        metaFile.writeText(o.toString())
    }

    fun upsertLessonsFromPull(recordsJson: String): Int {
        val root = JSONObject(recordsJson)
        val arr = root.optJSONArray("records") ?: JSONArray()
        val map = loadMap()
        var n = 0
        for (i in 0 until arr.length()) {
            val rec = arr.getJSONObject(i)
            val uid = rec.optString("uid")
            if (uid.isBlank()) continue
            map.put(uid, rec)
            n++
        }
        saveMap(map)
        return n
    }

    fun buildPushRecords(): JSONArray {
        val map = loadMap()
        val out = JSONArray()
        val keys = map.keys()
        while (keys.hasNext()) {
            out.put(map.getJSONObject(keys.next()))
        }
        return out
    }

    fun count(): Int = loadMap().length()

    private fun loadMap(): JSONObject {
        if (!lessonsFile.exists()) return JSONObject()
        return try {
            JSONObject(lessonsFile.readText())
        } catch (_: Exception) {
            JSONObject()
        }
    }

    private fun saveMap(map: JSONObject) {
        lessonsFile.writeText(map.toString())
    }
}
