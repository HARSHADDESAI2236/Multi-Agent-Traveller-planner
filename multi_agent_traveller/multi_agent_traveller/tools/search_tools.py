"""Data-fetching helpers used by agents.

These are mocked so the project runs out-of-the-box with no API keys.
Replace the bodies of these functions with real calls to services like
Amadeus / Skyscanner (flights), Booking.com / Expedia (hotels), or
OpenWeatherMap (weather) when you're ready to go live.
"""
from __future__ import annotations

import random
from typing import List

from utils.models import FlightOption, HotelOption, WeatherForecast


def search_flights(origin: str, destination: str, date: str) -> List[FlightOption]:
    airlines = ["SkyLine Air", "Pacific Wings", "Nimbus Airways"]
    return [
        FlightOption(
            airline=airline,
            departure=f"{origin} {date} 08:00",
            arrival=f"{destination} {date} 14:00",
            price=round(random.uniform(250, 900), 2),
            duration_hours=round(random.uniform(2, 14), 1),
        )
        for airline in airlines
    ]


def search_hotels(destination: str) -> List[HotelOption]:
    names = ["Harborview Hotel", "The Grand Plaza", "Traveler's Inn"]
    neighborhoods = ["Downtown", "Old Town", "Waterfront"]
    return [
        HotelOption(
            name=name,
            neighborhood=random.choice(neighborhoods),
            price_per_night=round(random.uniform(80, 400), 2),
            rating=round(random.uniform(3.5, 4.9), 1),
        )
        for name in names
    ]


def get_weather_forecast(destination: str, start_date: str, end_date: str) -> List[WeatherForecast]:
    summaries = ["Sunny", "Partly cloudy", "Light rain", "Clear skies"]
    return [
        WeatherForecast(
            date=f"Day {i + 1}",
            summary=random.choice(summaries),
            high_c=round(random.uniform(18, 32), 1),
            low_c=round(random.uniform(8, 18), 1),
        )
        for i in range(3)
    ]
