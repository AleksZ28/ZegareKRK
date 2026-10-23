package com.azurowski.zegarekrk.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class DepartureDto(
    val time: Long,
    val line: String,
    val headsign: String
)