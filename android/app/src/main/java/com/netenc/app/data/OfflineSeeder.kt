package com.netenc.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedInputStream
import java.util.zip.GZIPInputStream

/**
 * بارگذاری فهرست غنی از assets داخل Room (SQLite).
 * پشتیبانی از curriculum_index.json و curriculum_index.json.gz
 */
object OfflineSeeder {
    private const val META_SEEDED = "offline_seeded_v3"

    suspend fun ensureSeeded(context: Context): Int = withContext(Dispatchers.IO) {
        val dao = AppDatabase.get(context).lessonDao()
        val existing = dao.countActive()

        // اگر از قبل seed شده و محتوا واقعاً پر است، رد شو
        if (dao.getMeta(META_SEEDED) == "1" && existing > 1000) {
            val sample = dao.allActive().take(5)
            val filled = sample.count { it.fullContent.length > 80 }
            if (filled >= 3) return@withContext existing
        }

        val json = readCurriculumAsset(context) ?: return@withContext existing
        val root = JSONObject(json)
        val chapters = root.optJSONArray("chapters") ?: return@withContext existing

        val batch = mutableListOf<LessonEntity>()
        var inserted = 0
        for (ci in 0 until chapters.length()) {
            val ch = chapters.getJSONObject(ci)
            val subs = ch.optJSONArray("subchapters") ?: continue
            for (si in 0 until subs.length()) {
                val sub = subs.getJSONObject(si)
                val lessons = sub.optJSONArray("lessons") ?: continue
                for (li in 0 until lessons.length()) {
                    val les = lessons.getJSONObject(li)
                    val uid = les.optString("uid")
                    if (uid.isBlank()) continue
                    val summary = les.optString("summary")
                    val full = les.optString("full_content")
                    batch.add(
                        LessonEntity(
                            uid = uid,
                            entity = "lesson",
                            titleFa = les.optString("title_fa"),
                            titleEn = les.optString("title_en"),
                            tags = les.optString("level", "L0"),
                            summary = summary,
                            fullContent = full,
                            commands = les.optString("commands"),
                            examples = les.optString("examples"),
                            notes = les.optString("notes"),
                            lastUpdated = "1970-01-01T00:00:00Z",
                            contentHash = "offline-v3",
                            deviceId = "android-offline"
                        )
                    )
                    if (batch.size >= 150) {
                        dao.upsertAll(batch.toList())
                        inserted += batch.size
                        batch.clear()
                    }
                }
            }
        }
        if (batch.isNotEmpty()) {
            dao.upsertAll(batch)
            inserted += batch.size
        }
        dao.putMeta(SyncMetaEntity(META_SEEDED, "1"))
        dao.countActive()
    }

    private fun readCurriculumAsset(context: Context): String? {
        // اول JSON خام (همان چیزی که الان داخل APK است)
        try {
            context.assets.open("curriculum_index.json").use { raw ->
                return raw.bufferedReader(Charsets.UTF_8).readText()
            }
        } catch (_: Exception) { }

        // بعد gzip
        try {
            context.assets.open("curriculum_index.json.gz").use { raw ->
                return GZIPInputStream(BufferedInputStream(raw))
                    .bufferedReader(Charsets.UTF_8)
                    .readText()
            }
        } catch (_: Exception) { }

        return null
    }
}
