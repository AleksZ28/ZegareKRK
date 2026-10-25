package com.azurowski.zegarekrk.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class StopDto(
    val stop_id: String,
    val name: String,
    val distance: Double
)