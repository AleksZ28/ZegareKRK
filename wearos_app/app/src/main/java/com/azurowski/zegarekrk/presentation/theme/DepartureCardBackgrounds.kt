package com.azurowski.zegarekrk.presentation.theme

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color

object DepartureCardBackgrounds {
    val Already = Brush.linearGradient(
        colors = listOf(
            Color(0xFF2F323C),
            Color(0xFF3B3941),
            Color(0xFF4B4040),
            Color(0xFF703636)
        ),
        start = Offset(0f, 0f),
        end = Offset(Float.POSITIVE_INFINITY, 0f)
    )

    val Soon = Brush.linearGradient(
        colors = listOf(
            Color(0xFF2F323C),
            Color(0xFF393C41),
            Color(0xFF4B4740),
            Color(0xFF706536)
        ),
        start = Offset(0f, 0f),
        end = Offset(Float.POSITIVE_INFINITY, 0f)
    )

    val Later = Brush.linearGradient(
        colors = listOf(
            Color(0xFF2F323C),
            Color(0xFF393C41),
            Color(0xFF444B40),
            Color(0xFF577036)
        ),
        start = Offset(0f, 0f),
        end = Offset(Float.POSITIVE_INFINITY, 0f)
    )
}