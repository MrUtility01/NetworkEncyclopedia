package com.netenc.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedInputStream
import java.util.zip.GZIPInputStream

object OfflineSeeder {
    private const val META_SEEDED = "offline_seeded_v7"

    suspend fun ensureSeeded(context: Context): Int = withContext(Dispatchers.IO) {
        val dao = AppDatabase.get(context).lessonDao()
        val existing = dao.countActive()
        val filled = if (existing > 0) dao.countFilled() else 0
        if (dao.getMeta(META_SEEDED) == "1" && existing > 500 && filled > 200) {
            return@withContext existing
        }
        val json = readCurriculumAsset(context) ?: return@withContext existing
        val root = JSONObject(json)
        val chapters = root.optJSONArray("chapters") ?: return@withContext existing
        val batch = mutableListOf<LessonEntity>()
        for (ci in 0 until chapters.length()) {
            val ch = chapters.getJSONObject(ci)
            val chOrder = ch.optInt("order", ci + 1)
            val chTitle = ch.optString("title_fa")
            val subs = ch.optJSONArray("subchapters") ?: continue
            var lessonOrd = 0
            for (si in 0 until subs.length()) {
                val sub = subs.getJSONObject(si)
                val subTitle = sub.optString("title_fa")
                val lessons = sub.optJSONArray("lessons") ?: continue
                for (li in 0 until lessons.length()) {
                    val les = lessons.getJSONObject(li)
                    val uid = les.optString("uid")
                    if (uid.isBlank()) continue
                    lessonOrd++
                    batch.add(
                        LessonEntity(
                            uid = uid,
                            titleFa = les.optString("title_fa"),
                            titleEn = les.optString("title_en"),
                            tags = les.optString("level", "L0"),
                            summary = les.optString("summary"),
                            fullContent = les.optString("full_content"),
                            commands = les.optString("commands"),
                            examples = les.optString("examples"),
                            notes = les.optString("notes"),
                            lastUpdated = "2026-10-08T00:00:00Z",
                            contentHash = "offline-v7-deep",
                            deviceId = "android-offline",
                            chapterOrder = chOrder,
                            chapterTitle = chTitle,
                            subTitle = subTitle,
                            lessonOrder = lessonOrd
                        )
                    )
                    if (batch.size >= 50) {
                        dao.upsertAll(batch.toList())
                        batch.clear()
                    }
                }
            }
        }
        if (batch.isNotEmpty()) dao.upsertAll(batch)
        dao.putMeta(SyncMetaEntity(META_SEEDED, "1"))
        dao.countActive()
    }

    private fun readCurriculumAsset(context: Context): String? {
        try {
            context.assets.open("curriculum_index.json").use {
                return it.bufferedReader(Charsets.UTF_8).readText()
            }
        } catch (_: Exception) {}
        try {
            context.assets.open("curriculum_index.json.gz").use { raw ->
                return GZIPInputStream(BufferedInputStream(raw))
                    .bufferedReader(Charsets.UTF_8).readText()
            }
        } catch (_: Exception) {}
        return null
    }
}
