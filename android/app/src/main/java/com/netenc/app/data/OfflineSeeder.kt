package com.netenc.app.data

import android.content.Context
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedInputStream
import java.util.zip.GZIPInputStream

object OfflineSeeder {
    private const val TAG = "OfflineSeeder"
    private const val META_SEEDED = "offline_seeded_v22"

    suspend fun ensureSeeded(context: Context, force: Boolean = false): Int = withContext(Dispatchers.IO) {
        val dao = AppDatabase.get(context).lessonDao()
        try {
            val existing = dao.countActive()
            val filled = if (existing > 0) dao.countFilled() else 0
            val metaOk = dao.getMeta(META_SEEDED) == "1"
            if (!force && metaOk && existing >= 1000 && filled >= 500) {
                Log.i(TAG, "skip seed existing=$existing filled=$filled")
                return@withContext existing
            }

            val json = readCurriculumAsset(context)
            if (json.isNullOrBlank()) {
                Log.e(TAG, "curriculum asset missing or empty")
                return@withContext existing
            }

            val root = try {
                JSONObject(json)
            } catch (e: Exception) {
                Log.e(TAG, "json parse failed", e)
                return@withContext existing
            }
            val chapters = root.optJSONArray("chapters")
            if (chapters == null || chapters.length() == 0) {
                Log.e(TAG, "no chapters in asset")
                return@withContext existing
            }

            val all = ArrayList<LessonEntity>(6000)
            for (ci in 0 until chapters.length()) {
                val ch = chapters.optJSONObject(ci) ?: continue
                val chOrder = ch.optInt("order", ci + 1)
                val chTitle = ch.optString("title_fa").ifBlank { "فصل $chOrder" }
                val subs = ch.optJSONArray("subchapters") ?: continue
                var lessonOrd = 0
                for (si in 0 until subs.length()) {
                    val sub = subs.optJSONObject(si) ?: continue
                    val subTitle = sub.optString("title_fa").ifBlank { "بخش ${si + 1}" }
                    val lessons = sub.optJSONArray("lessons") ?: continue
                    for (li in 0 until lessons.length()) {
                        val les = lessons.optJSONObject(li) ?: continue
                        var uid = les.optString("uid")
                        if (uid.isBlank()) uid = "lesson:ch${chOrder}:s$si:l$li"
                        lessonOrd++
                        all.add(
                            LessonEntity(
                                uid = uid,
                                titleFa = les.optString("title_fa").ifBlank { "درس $lessonOrd" },
                                titleEn = les.optString("title_en"),
                                tags = les.optString("level", "L0"),
                                summary = les.optString("summary"),
                                fullContent = les.optString("full_content"),
                                commands = les.optString("commands"),
                                examples = les.optString("examples"),
                                notes = les.optString("notes"),
                                lastUpdated = "2026-10-13T15:00:00Z",
                                contentHash = "offline-v22",
                                deviceId = "android-offline",
                                chapterOrder = chOrder,
                                chapterTitle = chTitle,
                                subTitle = subTitle,
                                lessonOrder = lessonOrd
                            )
                        )
                    }
                }
            }

            if (all.isEmpty()) {
                Log.e(TAG, "parsed 0 lessons — keep old DB")
                return@withContext existing
            }

            Log.i(TAG, "parsed ${all.size} lessons from ${chapters.length()} chapters — writing DB")
            dao.clearAllLessons()
            var i = 0
            while (i < all.size) {
                val end = minOf(i + 100, all.size)
                dao.upsertAll(all.subList(i, end).toList())
                i = end
            }
            dao.putMeta(SyncMetaEntity(META_SEEDED, "1"))
            dao.putMeta(SyncMetaEntity("offline_seeded_v11", "0"))
            dao.putMeta(SyncMetaEntity("offline_seeded_v13", "0"))
            dao.putMeta(SyncMetaEntity("offline_seeded_v20", "0"))
            dao.putMeta(SyncMetaEntity("offline_seeded_v21", "0"))
            val n = dao.countActive()
            Log.i(TAG, "seed done count=$n")
            n
        } catch (e: Exception) {
            Log.e(TAG, "seed failed", e)
            try {
                dao.countActive()
            } catch (_: Exception) {
                0
            }
        }
    }

    private fun readCurriculumAsset(context: Context): String? {
        try {
            context.assets.open("curriculum_index.json").use {
                return it.bufferedReader(Charsets.UTF_8).readText()
            }
        } catch (e: Exception) {
            Log.w(TAG, "plain json missing: ${e.message}")
        }
        try {
            context.assets.open("curriculum_index.json.gz").use { raw ->
                return GZIPInputStream(BufferedInputStream(raw, 64 * 1024))
                    .bufferedReader(Charsets.UTF_8).readText()
            }
        } catch (e: Exception) {
            Log.e(TAG, "gz read failed", e)
        }
        return null
    }
}
