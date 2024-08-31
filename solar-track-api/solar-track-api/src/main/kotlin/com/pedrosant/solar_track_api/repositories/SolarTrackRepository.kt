package com.pedrosant.solar_track_api.repositories

import com.pedrosant.solar_track_api.models.SolarTrackData
import org.springframework.data.jpa.repository.JpaRepository

interface SolarTrackRepository:JpaRepository<SolarTrackData, Long> {
}