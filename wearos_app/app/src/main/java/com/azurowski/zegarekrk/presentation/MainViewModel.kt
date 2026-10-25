package com.azurowski.zegarekrk.presentation

import android.app.Application
import android.location.Location
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.azurowski.zegarekrk.data.api.TransitApi
import com.azurowski.zegarekrk.data.location.LocationClient
import com.azurowski.zegarekrk.presentation.model.DepartureUiModel
import com.azurowski.zegarekrk.presentation.model.StopUiModel
import com.azurowski.zegarekrk.presentation.utils.getDepartureState
import com.azurowski.zegarekrk.presentation.utils.getDepartureTime
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val _hasLocationPermission = MutableStateFlow(false)
    val hasLocationPermission: StateFlow<Boolean> = _hasLocationPermission

    private val _location = MutableStateFlow<Location?>(null)

    private val _stops = MutableStateFlow<List<StopUiModel>>(emptyList())
    val stops: StateFlow<List<StopUiModel>> = _stops

    private suspend fun fetchDepartures(stopId: String): List<DepartureUiModel>? {
        try {
            val res = TransitApi.getDepartures(stopId)
            val uiDepartures = res.map { departure ->
                val departureTime = getDepartureTime(departure.time)
                val line = departure.line
                val headsign = departure.headsign
                val state = getDepartureState(departureTime)
                return@map DepartureUiModel(line, headsign, departureTime, state)
            }
            Log.d("Departures", uiDepartures.toString())
            return uiDepartures
        } catch (e: Exception) {
            Log.e("Departures", "Error fetching departures: ${e.message}")
            return null
        }
    }

    private suspend fun getLocation() {
        val locationClient = LocationClient(getApplication())
        val location = locationClient.getCurrentLocation()
        _location.value = location
        Log.d("Location", location.toString())
    }

    private fun getStopsWithDepartures() {
        viewModelScope.launch {
            getLocation()
            if (_location.value != null) {
                val lat = _location.value!!.latitude
                val lon = _location.value!!.longitude
                val radius = 500 // TODO

                try {
                    val res = TransitApi.getStops(lat, lon, radius)

                    val uiStops = res.map { stop ->
                        val name = stop.name
                        val distance = stop.distance
                        val departures = fetchDepartures(stop.stop_id) ?: emptyList()
                        return@map StopUiModel(name, distance, departures)
                    }

                    _stops.value = uiStops
                    Log.d("Stops", res.toString())
                } catch (e: Exception) {
                    Log.e("Stops", "Error fetching stops: ${e.message}")
                }
            }
        }
    }

    fun onPermissionResult(isGranted: Boolean) {
        _hasLocationPermission.value = isGranted
        if (isGranted) {
            getStopsWithDepartures()
        }
    }
}