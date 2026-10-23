package com.azurowski.zegarekrk.presentation

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.azurowski.zegarekrk.data.api.TransitApi
import com.azurowski.zegarekrk.data.api.model.DepartureDto
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class MainViewModel: ViewModel() {
    private val _departures = MutableStateFlow<List<DepartureDto>>(emptyList())
    val departures: StateFlow<List<DepartureDto>> = _departures

    init {
        fetchDepartures()
    }

    private fun fetchDepartures() {
        viewModelScope.launch {
            try {
                _departures.value = TransitApi.getDepartures("stop_1_1") // for tests
                Log.d("Departures", _departures.value.toString())
            } catch (e: Exception) {
                Log.e("Departures", "Error fetching departures: ${e.message}")
            }
        }
    }
}