package com.azurowski.zegarekrk.presentation.utils

import androidx.compose.ui.graphics.Brush
import com.azurowski.zegarekrk.presentation.model.DepartureState
import com.azurowski.zegarekrk.presentation.theme.DepartureCardBackgrounds

fun getDepartureCardBackground(departureState: DepartureState): Brush {
    return when(departureState) {
        DepartureState.ALREADY -> DepartureCardBackgrounds.Already
        DepartureState.SOON -> DepartureCardBackgrounds.Soon
        else -> DepartureCardBackgrounds.Later
    }
}