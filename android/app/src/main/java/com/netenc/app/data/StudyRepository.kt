package com.netenc.app.data

import android.content.Context
import java.time.Instant
import java.time.temporal.ChronoUnit

class StudyRepository(context: Context) {
    private val dao = AppDatabase.get(context).studyDao()

    suspend fun mark(uid: String, action: String): StudyEntity {
        val old = dao.byUid(uid)
        var ease = old?.ease ?: 2.5
        var interval = old?.intervalHours ?: 1
        var times = old?.timesStudied ?: 0
        times += 1
        val now = Instant.now()
        val status: String
        val next: Instant
        when (action) {
            "studied" -> {
                interval = maxOf(1, (interval * ease).toInt())
                if (interval > 24 * 30) interval = 24 * 30
                status = if (times >= 3 && interval >= 24) "known" else "learning"
                next = now.plus(interval.toLong(), ChronoUnit.HOURS)
            }
            "again" -> {
                interval = 1
                status = "review"
                next = now.plus(1, ChronoUnit.HOURS)
            }
            else -> {
                interval = 1
                ease = maxOf(1.3, ease - 0.2)
                status = "learning"
                next = now.plus(1, ChronoUnit.HOURS)
            }
        }
        val row = StudyEntity(
            lessonUid = uid,
            status = status,
            ease = ease,
            intervalHours = interval,
            lastStudied = now.toString(),
            nextReview = next.toString(),
            timesStudied = times
        )
        dao.upsert(row)
        return row
    }

    suspend fun dueNow(limit: Int = 40): List<StudyEntity> =
        dao.due(Instant.now().toString(), limit)

    suspend fun stats(): Map<String, Int> = mapOf(
        "tracked" to dao.countAll(),
        "learning" to dao.countStatus("learning"),
        "known" to dao.countStatus("known"),
        "review" to dao.countStatus("review"),
        "due" to dueNow(500).size
    )
}
