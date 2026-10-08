package com.netenc.app.reminder

import android.content.Context
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import java.util.concurrent.TimeUnit

object ReminderScheduler {
    private const val UNIQUE = "netenc_review_periodic"

    fun scheduleHourly(context: Context) {
        scheduleMinutes(context, 60)
    }

    /** فاصله یادآوری به دقیقه — حداقل ۱۵ (محدودیت WorkManager) */
    fun scheduleMinutes(context: Context, minutes: Int) {
        val m = minutes.coerceIn(15, 24 * 60)
        val req = PeriodicWorkRequestBuilder<ReviewWorker>(m.toLong(), TimeUnit.MINUTES)
            .build()
        WorkManager.getInstance(context).enqueueUniquePeriodicWork(
            UNIQUE,
            ExistingPeriodicWorkPolicy.UPDATE,
            req
        )
    }

    fun cancel(context: Context) {
        WorkManager.getInstance(context).cancelUniqueWork(UNIQUE)
    }
}
