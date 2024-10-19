package com.pedrosant.solar_track_api.models

import java.time.LocalDateTime

data class SolarTrackData(
    val id:Long? = null,
    val latitude:Double,
    val longitude:Double,
    val solarRadiation:Double,
    val datetime:LocalDateTime = LocalDateTime.now()
)
