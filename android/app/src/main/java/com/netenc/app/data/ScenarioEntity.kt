package com.netenc.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "scenarios")
data class ScenarioEntity(
    @PrimaryKey val code: String,
    val titleFa: String = "",
    val titleEn: String = "",
    val category: String = "Capstone",
    val level: String = "L4",
    val difficulty: String = "خبره",
    val users: Int = 0,
    val sites: Int = 1,
    val vendors: String = "",
    val businessContext: String = "",
    val requirements: String = "",
    val constraintsText: String = "",
    val initialState: String = "",
    val incident: String = "",
    val symptoms: String = "",
    val objectives: String = "",
    val tasks: String = "",
    val hints: String = "",
    val expectedResult: String = "",
    val solution: String = "",
    val verification: String = "",
    val skillsRequired: String = "",
    val estimatedHours: Int = 8
)
