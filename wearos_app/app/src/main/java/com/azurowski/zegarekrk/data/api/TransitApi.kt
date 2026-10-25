package com.azurowski.zegarekrk.data.api
import com.azurowski.zegarekrk.data.api.model.DepartureDto
import com.azurowski.zegarekrk.data.api.model.StopDto
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.cio.CIO
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.request.get
import io.ktor.client.statement.HttpResponse
import io.ktor.serialization.kotlinx.json.json

object TransitApi {
    private val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json()
        }
    }

    suspend fun getDepartures(stopId: String): List<DepartureDto> {
        val response: HttpResponse = client.get("http://192.168.0.134:8000/departures/$stopId") // local URL
        return response.body()
    }

    suspend fun getStops(lat: Double, lon: Double, radius: Int = 500): List<StopDto> {
        val response: HttpResponse = client.get("http://192.168.0.134:8000/stops?lat=$lat&lon=$lon&radius=$radius") // local URL
        return response.body()
    }
}