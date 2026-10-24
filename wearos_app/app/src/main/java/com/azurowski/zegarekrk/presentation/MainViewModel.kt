package com.azurowski.zegarekrk.presentation

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.azurowski.zegarekrk.data.api.TransitApi
import com.azurowski.zegarekrk.presentation.model.DepartureUiModel
import com.azurowski.zegarekrk.presentation.utils.getDepartureState
import com.azurowski.zegarekrk.presentation.utils.getDepartureTime
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class MainViewModel: ViewModel() {
    private val _departures = MutableStateFlow<List<DepartureUiModel>>(emptyList())
    val departures: StateFlow<List<DepartureUiModel>> = _departures

    init {
        fetchDepartures()
    }

    private fun fetchDepartures() {
        viewModelScope.launch {
            try {
                val res = TransitApi.getDepartures("stop_204_12619") // for tests
                val uiDepartures = res.map { departure ->
                    val departureTime = getDepartureTime(departure.time)
                    val line = departure.line
                    val headsign = departure.headsign
                    val state = getDepartureState(departureTime)
                    return@map DepartureUiModel(line, headsign, departureTime, state)
                }
                _departures.value = uiDepartures
                Log.d("Departures", _departures.value.toString())
            } catch (e: Exception) {
                Log.e("Departures", "Error fetching departures: ${e.message}")
            }
        }
    }
}