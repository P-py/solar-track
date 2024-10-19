package com.pedrosant.solar_track_api.services

import com.pedrosant.solar_track_api.mappers.SolarTrackMapper
import com.pedrosant.solar_track_api.models.SolarTrackData
import com.pedrosant.solar_track_api.models.SolarTrackResponse
import com.pedrosant.solar_track_api.repositories.SolarTrackRepository
import org.springframework.stereotype.Service

@Service
class SolarTrackService(
    private val solarTrackRepository:SolarTrackRepository,
    private val mapper:SolarTrackMapper
){
    fun create(solarTrackData:SolarTrackData):SolarTrackResponse{
        solarTrackRepository.save(solarTrackData)
        return mapper.mapToResponse(solarTrackData)
    }
}