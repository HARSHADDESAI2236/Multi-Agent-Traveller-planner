from __future__ import annotations

import re
from datetime import date, timedelta
from typing import List

from agents.base_agent import BaseAgent
from services.ollama_service import ask_ollama
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
    """Builds a day-by-day itinerary using Ollama, with a fallback."""

    name = "itinerary_agent"

    def _llm_activities(self, request, day_number, num_days, activity_count, weather_note):
        prompt = (
            f"You are a travel planner. Suggest exactly {activity_count} activities "
            f"for day {day_number} of a {num_days}-day trip to {request.destination}. "
            f"{weather_note}"
            "Reply with one activity per line, short (under 12 words), "
            "no numbering, no bullets, no extra text."
        )
        reply = ask_ollama(prompt)
        if reply.startswith("Error:"):
            return []
        lines = [re.sub(r"^[\s\-\*\d\.\)]+", "", ln).strip() for ln in reply.splitlines()]
        return [ln for ln in lines if ln][:activity_count]

    def run(self, request: TripRequest, weather: List[WeatherForecast]) -> List[ItineraryDay]:
        self.logger.info("Building itinerary for %s", request.destination)
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
            # Tell the model about the weather (change "condition" if your field is named differently)
            condition = getattr(weather[i], "condition", None) if i < len(weather) else None
            weather_note = f"The weather will be: {condition}. " if condition else ""

            activities = self._llm_activities(
                request, i + 1, num_days, activity_count, weather_note
            )

            # Fallback if Ollama failed or returned nothing
            if not activities:
                self.logger.warning("Ollama failed, using default activities")
                start_idx = (i * activity_count) % len(_ACTIVITY_BANK)
                activities = [
                    _ACTIVITY_BANK[(start_idx + j) % len(_ACTIVITY_BANK)]
                    for j in range(activity_count)
                ]

            if request.preferences:
                activities.append(f"Preference-based activity: {request.preferences[0]}")

            day_date = (
                weather[i].date if i < len(weather)
                else (start + timedelta(days=i)).isoformat() if start
                else f"Day {i + 1}"
            )
            days.append(ItineraryDay(day_number=i + 1, date=day_date, activities=activities))
        return days