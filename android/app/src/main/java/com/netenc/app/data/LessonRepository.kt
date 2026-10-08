package com.netenc.app.data

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

class LessonRepository(context: Context) {
    private val dao = AppDatabase.get(context).lessonDao()

    suspend fun count(): Int = dao.countActive()

    suspend fun getLastSync(): String = dao.getMeta("last_sync") ?: ""

    suspend fun setLastSync(iso: String) {
        dao.putMeta(SyncMetaEntity("last_sync", iso))
    }

    suspend fun upsertFromPullJson(recordsJson: String): Int {
        val root = JSONObject(recordsJson)
        val arr = root.optJSONArray("records") ?: JSONArray()
        val list = mutableListOf<LessonEntity>()
        for (i in 0 until arr.length()) {
            val r = arr.getJSONObject(i)
            val uid = r.optString("uid")
            if (uid.isBlank()) continue
            list.add(
                LessonEntity(
                    uid = uid,
                    entity = r.optString("entity", "lesson"),
                    titleFa = r.optString("title_fa", r.optString("titleFa", "")),
                    titleEn = r.optString("title_en", r.optString("titleEn", "")),
                    tags = r.optString("tags", ""),
                    summary = r.optString("summary", ""),
                    fullContent = r.optString("full_content", r.optString("fullContent", "")),
                    commands = r.optString("commands", ""),
                    examples = r.optString("examples", ""),
                    notes = r.optString("notes", ""),
                    metaJson = r.optString("meta_json", r.optString("metaJson", "{}")),
                    searchQuery = r.optString("search_query", ""),
                    learningObjectives = r.optString("learning_objectives", ""),
                    sourceStatus = r.optString("source_status", "unverified"),
                    lastUpdated = r.optString("last_updated", ""),
                    contentHash = r.optString("content_hash", ""),
                    deviceId = r.optString("device_id", ""),
                    deleted = r.optBoolean("deleted", false)
                )
            )
        }
        if (list.isNotEmpty()) dao.upsertAll(list)
        return list.size
    }

    suspend fun buildPushArray(): JSONArray {
        val out = JSONArray()
        for (e in dao.allForPush()) {
            out.put(
                JSONObject()
                    .put("uid", e.uid)
                    .put("entity", e.entity)
                    .put("title_fa", e.titleFa)
                    .put("title_en", e.titleEn)
                    .put("tags", e.tags)
                    .put("summary", e.summary)
                    .put("full_content", e.fullContent)
                    .put("commands", e.commands)
                    .put("examples", e.examples)
                    .put("notes", e.notes)
                    .put("meta_json", e.metaJson)
                    .put("search_query", e.searchQuery)
                    .put("learning_objectives", e.learningObjectives)
                    .put("source_status", e.sourceStatus)
                    .put("last_updated", e.lastUpdated)
                    .put("content_hash", e.contentHash)
                    .put("device_id", e.deviceId)
                    .put("deleted", e.deleted)
            )
        }
        return out
    }
}
