package com.azurowski.zegarekrk.presentation.utils

fun getDepartureTime(timestamp: Long): String {
    val currentDateTime: java.util.Date = java.util.Date()
    val currentTimestamp: Long = currentDateTime.time
    val timeDifference: Long = timestamp * 1000 - currentTimestamp

    val minutes: Long = timeDifference / (1000 * 60)

    return if (minutes.toInt() == 0) {
        "Teraz"
    } else {
        "$minutes min"
    }
}