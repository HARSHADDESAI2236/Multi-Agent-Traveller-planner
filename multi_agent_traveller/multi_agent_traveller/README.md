# Multi-Agent Traveller

A multi-agent AI system for trip planning. A **Coordinator Agent** orchestrates
specialized agents (Flights, Hotels, Weather, Itinerary) to research and
assemble a complete travel plan from a single natural-language request.

## Project Structure

```
multi_agent_traveller/
├── main.py                  # Entry point / CLI
├── requirements.txt         # Python dependencies
├── .env.example              # Environment variable template
├── config/
│   ├── __init__.py
│   └── settings.py          # App-wide configuration & API keys
├── agents/
│   ├── __init__.py
│   ├── base_agent.py        # Abstract base class all agents inherit from
│   ├── coordinator_agent.py # Orchestrates the other agents
│   ├── flight_agent.py      # Searches / recommends flights
│   ├── hotel_agent.py       # Searches / recommends hotels
│   ├── weather_agent.py     # Fetches weather forecasts for the destination
│   └── itinerary_agent.py   # Builds a day-by-day itinerary
├── tools/
│   ├── __init__.py
│   ├── search_tools.py      # Web/API search helper functions used by agents
│   └── booking_tools.py     # (Stub) booking / reservation helper functions
├── utils/
│   ├── __init__.py
│   ├── logger.py            # Centralized logging setup
│   └── models.py            # Shared dataclasses / pydantic models
├── data/
│   └── sample_request.json  # Example input for a trip request
└── tests/
    ├── __init__.py
    ├── test_agents.py
    └── test_coordinator.py
```

## How it works

1. `main.py` reads a trip request (destination, dates, budget, preferences).
2. `CoordinatorAgent` breaks the request into subtasks and dispatches them
   to `FlightAgent`, `HotelAgent`, and `WeatherAgent` (in parallel, if desired).
3. Each specialized agent returns structured results (see `utils/models.py`).
4. `ItineraryAgent` consumes all results and produces a final day-by-day plan.
5. `CoordinatorAgent` returns the combined `TripPlan` to the caller.

## Getting started

```bash
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in your API keys
python main.py --destination "Tokyo" --start-date 2026-11-01 --end-date 2026-11-07
```

## Extending

- Add a new agent by subclassing `BaseAgent` in `agents/base_agent.py` and
  registering it inside `CoordinatorAgent`.
- Swap the LLM provider or add real API integrations (flight/hotel search
  APIs, weather APIs) inside `tools/search_tools.py`.
- Add tests for any new agent under `tests/`.

## Notes

This scaffold ships with working control flow and clear extension points,
but the actual flight/hotel/weather lookups in `tools/search_tools.py` are
stubbed with mock data — wire in real APIs (e.g. Amadeus, Skyscanner,
OpenWeatherMap) and your LLM provider of choice (Anthropic, OpenAI, etc.)
to make it fully functional.
