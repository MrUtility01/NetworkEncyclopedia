package com.netenc.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "lessons")
data class LessonEntity(
    @PrimaryKey val uid: String,
    val entity: String = "lesson",
    val titleFa: String = "",
    val titleEn: String = "",
    val tags: String = "",
    val summary: String = "",
    val fullContent: String = "",
    val commands: String = "",
    val examples: String = "",
    val notes: String = "",
    val metaJson: String = "{}",
    val searchQuery: String = "",
    val learningObjectives: String = "",
    val sourceStatus: String = "unverified",
    val lastUpdated: String = "",
    val contentHash: String = "",
    val deviceId: String = "",
    val deleted: Boolean = false,
    // سلسله‌مراتب برای درخت
    val chapterOrder: Int = 0,
    val chapterTitle: String = "",
    val subTitle: String = "",
    val lessonOrder: Int = 0
)
