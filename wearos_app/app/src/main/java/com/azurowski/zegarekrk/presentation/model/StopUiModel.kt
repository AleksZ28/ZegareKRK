package com.azurowski.zegarekrk.presentation.model

data class StopUiModel(
    val name: String,
    val distance: Double,
    val departures: List<DepartureUiModel>
)
