package com.azurowski.zegarekrk.presentation.utils

import androidx.compose.ui.graphics.Brush
import com.azurowski.zegarekrk.presentation.theme.DepartureCardBackgrounds

fun getDepartureCardBackground(departureState: String): Brush {
    return when{
        departureState == "already" -> DepartureCardBackgrounds.Already
        departureState == "soon" -> DepartureCardBackgrounds.Soon
        else -> DepartureCardBackgrounds.Later
    }
}