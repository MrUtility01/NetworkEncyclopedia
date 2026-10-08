package com.netenc.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "study_progress")
data class StudyEntity(
    @PrimaryKey val lessonUid: String,
    val status: String = "new", // new | learning | known | review
    val ease: Double = 2.5,
    val intervalHours: Int = 1,
    val lastStudied: String = "",
    val nextReview: String = "",
    val timesStudied: Int = 0,
    val notes: String = ""
)
