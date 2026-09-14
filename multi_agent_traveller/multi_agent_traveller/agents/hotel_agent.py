from __future__ import annotations

from typing import List

from agents.base_agent import BaseAgent
from tools.search_tools import search_hotels
from utils.models import HotelOption, TripRequest


class HotelAgent(BaseAgent):
    name = "hotel_agent"

    def run(self, request: TripRequest) -> List[HotelOption]:
        self.logger.info("Searching hotels in %s", request.destination)
        hotels = search_hotels(request.destination)
        hotels.sort(key=lambda h: h.price_per_night)
        return hotels
