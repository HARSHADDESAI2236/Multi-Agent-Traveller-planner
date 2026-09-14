from __future__ import annotations

from typing import List

from agents.base_agent import BaseAgent
from utils.models import ItineraryDay, TripRequest, WeatherForecast

_ACTIVITY_BANK = [
    "Explore the historic old town",
    "Visit the main art museum",
    "Try local street food at the night market",
    "Take a guided walking tour",
    "Relax at a nearby park or waterfront",
    "Visit a popular viewpoint or landmark",
    "Shop at the local markets",
]


class ItineraryAgent(BaseAgent):
    """Builds a simple day-by-day itinerary.

    In a production system this would call an LLM with the trip request,
    weather forecast, and traveler preferences to generate a tailored plan.
    Here it's a lightweight deterministic placeholder so the project runs
    without any API keys configured.
    """

    name = "itinerary_agent"

    def run(self, request: TripRequest, weather: List[WeatherForecast]) -> List[ItineraryDay]:
        self.logger.info("Building itinerary for %s", request.destination)
        num_days = max(len(weather), 3)
        days = []
        for i in range(num_days):
            activities = _ACTIVITY_BANK[i % len(_ACTIVITY_BANK): i % len(_ACTIVITY_BANK) + 2]
            if request.preferences:
                activities.append(f"Preference-based activity: {request.preferences[0]}")
            days.append(
                ItineraryDay(
                    day_number=i + 1,
                    date=weather[i].date if i < len(weather) else f"Day {i + 1}",
                    activities=activities,
                )
            )
        return days
