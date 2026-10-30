from __future__ import annotations

from datetime import date, timedelta
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
        # Use the requested trip duration instead of forcing at least three days.
        try:
            start = date.fromisoformat(request.start_date)
            end = date.fromisoformat(request.end_date)
            num_days = max(1, (end - start).days)
        except (TypeError, ValueError):
            num_days = max(1, len(weather))
            start = None

        pace = (getattr(request, "pace", "Balanced") or "Balanced").lower()
        activity_count = 1 if pace == "relaxed" else 3 if pace == "packed" else 2
        days = []
        for i in range(num_days):
            start_idx = (i * activity_count) % len(_ACTIVITY_BANK)
            activities = [_ACTIVITY_BANK[(start_idx + j) % len(_ACTIVITY_BANK)] for j in range(activity_count)]
            if request.preferences:
                activities.append(f"Preference-based activity: {request.preferences[0]}")
            day_date = weather[i].date if i < len(weather) else (start + timedelta(days=i)).isoformat() if start else f"Day {i + 1}"
            days.append(
                ItineraryDay(
                    day_number=i + 1,
                    date=day_date,
                    activities=activities,
                )
            )
        return days
