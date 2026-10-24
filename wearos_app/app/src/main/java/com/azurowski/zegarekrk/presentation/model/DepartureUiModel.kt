package com.azurowski.zegarekrk.presentation.model

enum class DepartureState {
    ALREADY,
    SOON,
    LATER
}

data class DepartureUiModel(
    val line: String,
    val headsign: String,
    val departureTime: String,
    val state: DepartureState
)
