package com.pedrosant.solar_track_api.controllers

import com.pedrosant.solar_track_api.models.SolarTrackData
import com.pedrosant.solar_track_api.models.SolarTrackResponse
import com.pedrosant.solar_track_api.services.SolarTrackService
import jakarta.transaction.Transactional
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.util.UriComponentsBuilder
import javax.validation.Valid

@RestController
@RequestMapping("/solar-track")
class SolarTrackController(
    private val service:SolarTrackService
){
    @PostMapping("/data")
    @Transactional
    fun createNewData(
        @RequestBody @Valid solarTrackData:SolarTrackData, uriBuilder: UriComponentsBuilder
    ):ResponseEntity<SolarTrackResponse>{
        val response = service.create(solarTrackData)
        val uri = uriBuilder.path("/solar-track/data/${response.solarTrackData.id}")
            .build()
            .toUri()
        return ResponseEntity.created(uri).body(response)
    }
}