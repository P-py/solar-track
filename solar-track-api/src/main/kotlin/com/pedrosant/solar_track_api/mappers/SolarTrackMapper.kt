package com.pedrosant.solar_track_api.mappers

import com.pedrosant.solar_track_api.models.SolarTrackData
import com.pedrosant.solar_track_api.models.SolarTrackResponse
import com.pedrosant.solar_track_api.services.SolarTrackService
import org.springframework.stereotype.Component

@Component
class SolarTrackMapper(private val solarTrackService:SolarTrackService):Mapper<SolarTrackData, SolarTrackResponse>{
    override fun mapToResponse(c: SolarTrackData): SolarTrackResponse {
        return SolarTrackResponse(
            message = "Solar data successfully added to database.",
            solarTrackData = SolarTrackData(
                solarRadiation = c.solarRadiation,
                datetime = c.datetime,
                latitude = c.latitude,
                longitude = c.longitude
            )
        )
    }
}