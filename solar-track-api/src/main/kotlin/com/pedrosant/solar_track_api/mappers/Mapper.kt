package com.pedrosant.solar_track_api.mappers

interface Mapper<C, R> {
    fun mapToResponse(c:C):R
}