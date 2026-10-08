package com.netenc.app.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface ScenarioDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(items: List<ScenarioEntity>)

    @Query("SELECT * FROM scenarios ORDER BY code")
    suspend fun all(): List<ScenarioEntity>

    @Query("SELECT * FROM scenarios WHERE code = :code LIMIT 1")
    suspend fun byCode(code: String): ScenarioEntity?

    @Query("SELECT COUNT(*) FROM scenarios")
    suspend fun count(): Int
}
