package com.netenc.app.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface LessonDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(items: List<LessonEntity>)

    @Query("SELECT * FROM lessons WHERE deleted = 0 ORDER BY titleFa")
    suspend fun allActive(): List<LessonEntity>

    @Query("SELECT * FROM lessons WHERE uid = :uid LIMIT 1")
    suspend fun byUid(uid: String): LessonEntity?

    @Query("SELECT COUNT(*) FROM lessons WHERE deleted = 0")
    suspend fun countActive(): Int

    @Query("SELECT * FROM lessons WHERE deleted = 0")
    suspend fun allForPush(): List<LessonEntity>

    @Query("SELECT value FROM sync_meta WHERE key = :key LIMIT 1")
    suspend fun getMeta(key: String): String?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun putMeta(row: SyncMetaEntity)
}
