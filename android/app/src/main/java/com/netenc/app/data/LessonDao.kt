package com.netenc.app.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface LessonDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(items: List<LessonEntity>)

    @Query("SELECT * FROM lessons WHERE deleted = 0 ORDER BY chapterOrder, lessonOrder, titleFa")
    suspend fun allActive(): List<LessonEntity>

    @Query("SELECT * FROM lessons WHERE uid = :uid LIMIT 1")
    suspend fun byUid(uid: String): LessonEntity?

    @Query("SELECT COUNT(*) FROM lessons WHERE deleted = 0")
    suspend fun countActive(): Int

    @Query("SELECT COUNT(*) FROM lessons WHERE deleted = 0 AND length(fullContent) > 80")
    suspend fun countFilled(): Int

    @Query("SELECT * FROM lessons WHERE deleted = 0")
    suspend fun allForPush(): List<LessonEntity>

    @Query(
        """SELECT * FROM lessons WHERE deleted = 0 AND (
            titleFa LIKE '%' || :q || '%' OR
            summary LIKE '%' || :q || '%' OR
            fullContent LIKE '%' || :q || '%' OR
            chapterTitle LIKE '%' || :q || '%' OR
            subTitle LIKE '%' || :q || '%'
        ) ORDER BY chapterOrder, lessonOrder LIMIT 200"""
    )
    suspend fun search(q: String): List<LessonEntity>

    @Query("SELECT DISTINCT chapterOrder, chapterTitle FROM lessons WHERE deleted = 0 ORDER BY chapterOrder")
    suspend fun chapters(): List<ChapterRow>

    @Query("SELECT * FROM lessons WHERE deleted = 0 AND chapterOrder = :co ORDER BY lessonOrder, titleFa")
    suspend fun byChapter(co: Int): List<LessonEntity>

    @Query("SELECT value FROM sync_meta WHERE key = :key LIMIT 1")
    suspend fun getMeta(key: String): String?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun putMeta(row: SyncMetaEntity)
}

data class ChapterRow(
    val chapterOrder: Int,
    val chapterTitle: String
)
