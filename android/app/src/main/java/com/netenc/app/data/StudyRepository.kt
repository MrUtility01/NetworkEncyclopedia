package com.netenc.app.data

import android.content.Context
import java.time.Instant
import java.time.temporal.ChronoUnit
import kotlin.math.max
import kotlin.math.roundToInt

/**
 * SRS شبیه SM-2:
 * again | hard | good | easy
 * فاصله‌ها بر حسب ساعت؛ سقف ۳۰ روز.
 */
class StudyRepository(context: Context) {
    private val dao = AppDatabase.get(context).studyDao()
    private val prefs = context.getSharedPreferences("netenc_study", Context.MODE_PRIVATE)

    suspend fun mark(uid: String, action: String): StudyEntity {
        val old = dao.byUid(uid)
        var ease = old?.ease ?: 2.5
        var interval = old?.intervalHours ?: 0
        var times = (old?.timesStudied ?: 0) + 1
        val now = Instant.now()
        val status: String
        val next: Instant

        when (action) {
            "again", "forgot" -> {
                ease = max(1.3, ease - 0.25)
                interval = 1
                status = "learning"
                next = now.plus(1, ChronoUnit.HOURS)
            }
            "hard" -> {
                ease = max(1.3, ease - 0.1)
                interval = if (interval <= 0) 6 else max(3, (interval * 1.2).roundToInt())
                status = "review"
                next = now.plus(interval.toLong(), ChronoUnit.HOURS)
            }
            "good", "studied" -> {
                interval = when {
                    interval <= 0 -> 24
                    interval < 24 -> 24
                    else -> max(24, (interval * ease).roundToInt())
                }
                if (interval > 24 * 30) interval = 24 * 30
                status = if (times >= 3 && interval >= 72) "known" else "learning"
                next = now.plus(interval.toLong(), ChronoUnit.HOURS)
            }
            "easy" -> {
                ease = minOf(3.0, ease + 0.15)
                interval = when {
                    interval <= 0 -> 72
                    else -> max(48, (interval * ease * 1.3).roundToInt())
                }
                if (interval > 24 * 45) interval = 24 * 45
                status = if (times >= 2) "known" else "learning"
                next = now.plus(interval.toLong(), ChronoUnit.HOURS)
            }
            else -> {
                interval = 1
                status = "review"
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
        recordDailyActivity()
        return row
    }

    suspend fun dueNow(limit: Int = 40): List<StudyEntity> =
        dao.due(Instant.now().toString(), limit)

    suspend fun stats(): Map<String, Int> = mapOf(
        "tracked" to dao.countAll(),
        "learning" to dao.countStatus("learning"),
        "known" to dao.countStatus("known"),
        "review" to dao.countStatus("review"),
        "due" to dueNow(500).size,
        "streak" to currentStreak(),
        "today" to todayCount(),
        "goal" to dailyGoal()
    )

    fun dailyGoal(): Int = prefs.getInt("daily_goal", 15)

    fun setDailyGoal(n: Int) {
        prefs.edit().putInt("daily_goal", n.coerceIn(5, 100)).apply()
    }

    fun todayCount(): Int {
        val key = "day_" + java.time.LocalDate.now().toString()
        return prefs.getInt(key, 0)
    }

    private fun recordDailyActivity() {
        val today = java.time.LocalDate.now().toString()
        val key = "day_$today"
        val n = prefs.getInt(key, 0) + 1
        prefs.edit().putInt(key, n).apply()
        val last = prefs.getString("last_active_day", "")
        val yesterday = java.time.LocalDate.now().minusDays(1).toString()
        var streak = prefs.getInt("streak", 0)
        when (last) {
            today -> { }
            yesterday -> streak += 1
            else -> streak = 1
        }
        prefs.edit().putString("last_active_day", today).putInt("streak", streak).apply()
    }

    fun currentStreak(): Int = prefs.getInt("streak", 0)

    fun goalReached(): Boolean = todayCount() >= dailyGoal()
}
