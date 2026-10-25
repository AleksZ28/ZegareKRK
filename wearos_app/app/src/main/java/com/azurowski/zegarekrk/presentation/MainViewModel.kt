package com.azurowski.zegarekrk.presentation

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.azurowski.zegarekrk.data.api.TransitApi
import com.azurowski.zegarekrk.data.location.LocationClient
import com.azurowski.zegarekrk.presentation.model.DepartureUiModel
import com.azurowski.zegarekrk.presentation.utils.getDepartureState
import com.azurowski.zegarekrk.presentation.utils.getDepartureTime
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val _departures = MutableStateFlow<List<DepartureUiModel>>(emptyList())
    val departures: StateFlow<List<DepartureUiModel>> = _departures

    private val _hasLocationPermission = MutableStateFlow(false)
    val hasLocationPermission: StateFlow<Boolean> = _hasLocationPermission

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

    fun getLocation() {
        viewModelScope.launch {
            val locationClient = LocationClient(getApplication())
            val location = locationClient.getCurrentLocation()
            Log.d("Location", location.toString())
        }
    }

    fun onPermissionResult(isGranted: Boolean) {
        _hasLocationPermission.value = isGranted
        if (isGranted) {
            getLocation()
        }
    }
}