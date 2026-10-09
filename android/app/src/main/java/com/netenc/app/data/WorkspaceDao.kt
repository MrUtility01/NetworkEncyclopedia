package com.netenc.app.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface WorkspaceDao {
    @Query("SELECT * FROM tasks ORDER BY done ASC, priority DESC, lastUpdated DESC")
    suspend fun allTasks(): List<TaskEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertTask(item: TaskEntity)

    @Query("DELETE FROM tasks WHERE uid = :uid")
    suspend fun deleteTask(uid: String)

    @Query("SELECT * FROM notes ORDER BY lastUpdated DESC")
    suspend fun allNotes(): List<NoteEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertNote(item: NoteEntity)

    @Query("DELETE FROM notes WHERE uid = :uid")
    suspend fun deleteNote(uid: String)

    @Query("SELECT * FROM vault_items ORDER BY title ASC")
    suspend fun allVault(): List<VaultEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertVault(item: VaultEntity)

    @Query("DELETE FROM vault_items WHERE uid = :uid")
    suspend fun deleteVault(uid: String)
}
