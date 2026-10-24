package com.azurowski.zegarekrk.presentation.utils

import com.azurowski.zegarekrk.presentation.model.DepartureState

fun getDepartureState(departureTime: String): DepartureState {
    if (departureTime == "Teraz") {
        return DepartureState.ALREADY
    }

    val minutes = departureTime.substringBefore(" ").toIntOrNull()

    return when {
        minutes == null -> DepartureState.LATER
        minutes < 0 -> DepartureState.ALREADY
        minutes < 5 -> DepartureState.SOON
        else -> DepartureState.LATER
    }
}