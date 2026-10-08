package com.netenc.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedInputStream
import java.util.zip.GZIPInputStream

/** بارگذاری فهرست ۶۳ فصل از assets — بدون نیاز به سرور */
object OfflineSeeder {
    private const val ASSET = "curriculum_index.json.gz"
    private const val META_SEEDED = "offline_seeded_v1"

    suspend fun ensureSeeded(context: Context): Int = withContext(Dispatchers.IO) {
        val repo = LessonRepository(context)
        val existing = repo.count()
        if (existing > 100) return@withContext existing

        val dao = AppDatabase.get(context).lessonDao()
        if (dao.getMeta(META_SEEDED) == "1" && existing > 0) return@withContext existing

        val json = readAssetGzip(context, ASSET) ?: return@withContext existing
        val root = JSONObject(json)
        val chapters = root.optJSONArray("chapters") ?: return@withContext existing
        val batch = mutableListOf<LessonEntity>()
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
                    val titleFa = les.optString("title_fa")
                    batch.add(
                        LessonEntity(
                            uid = uid,
                            entity = "lesson",
                            titleFa = titleFa,
                            titleEn = les.optString("title_en"),
                            summary = "نسخه آفلاین — $titleFa",
                            fullContent = "این درس به‌صورت آفلاین روی گوشی موجود است.\n\nعنوان: $titleFa\n\nبرای دریافت متن کامل‌تر می‌توانید (اختیاری) با ویندوز روی همان Wi‑Fi همگام‌سازی کنید.",
                            lastUpdated = "1970-01-01T00:00:00Z",
                            contentHash = "offline-seed",
                            deviceId = "android-offline"
                        )
                    )
                    if (batch.size >= 400) {
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

    private fun readAssetGzip(context: Context, name: String): String? {
        return try {
            context.assets.open(name).use { raw ->
                GZIPInputStream(BufferedInputStream(raw)).bufferedReader(Charsets.UTF_8).readText()
            }
        } catch (_: Exception) {
            null
        }
    }
}
