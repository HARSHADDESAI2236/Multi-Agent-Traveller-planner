<<<<<<< HEAD
# Multi-Agent-Traveller-planner
Collaboration Project
=======
# TravelMate — Original UI + Enhanced Features

This package starts from the original TravelMate Streamlit application and keeps its existing homepage, destination cards, typography, colors, navigation, and trip-result layout. The changes are additive: an animated destination search bar with a custom animated anime travel-guide illustration, searchable curated destinations, arbitrary-location Google Maps links, hotel links, trip preference controls, duplicate-submit protection, budget guidance, exports, accessibility-aware motion polish, and stronger tests.

## Features added

- **Animated location search:** search curated destinations by name, description, or highlights; suggestions are case-insensitive. Search any other city/place and open it in Google Maps, or create a trip plan for that custom destination.
- **Anime travel guide:** a lightweight inline SVG character with floating, hair-sway, blinking, and twinkle animations. It uses no extra image download and respects reduced-motion preferences.
- **Hotel discovery:** each recommended hotel has a Google Maps location search and a Google photos/reviews search. These open real Google search results; the app does not claim those results are verified bookings.
- **Trip controls:** relaxed/balanced/packed pace and budget/comfort/luxury accommodation preference.
- **Trip duration fix:** the itinerary is generated for the actual requested number of days, including one-day trips, rather than forcing at least three days.
- **Double-submit protection:** identical trip inputs reuse the generated plan within the current Streamlit session instead of calling the agents again.
- **Budget snapshot:** estimated flights/accommodation plus clearly labeled suggested food, local transport, activity, and contingency allocations.
- **Export:** JSON, TXT, PDF, and DOCX itinerary downloads.
- **Motion and accessibility:** refined hover/fade effects and support for `prefers-reduced-motion`; the original design system remains in place.
- **Input checks:** required locations, date order, budget, and traveler count validation.
- **Secret hygiene:** `.env` and virtual environments are excluded; `.env.example` contains placeholders only.

## Run on Windows PowerShell

Open PowerShell in the extracted `TravelMate_Original_UI_Enhanced` folder. This package puts `app.py` at the project root to avoid overly long nested Windows paths.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.

If the Python launcher does not have Python 3.12 installed, install a supported Python 3.12+ version and use `python -m venv .venv` instead.

## Run tests

```powershell
python -m pytest -q
```

The included suite currently contains 17 passing unit/regression tests, including destination-search matching, arbitrary location URL encoding, export generation, validation edge cases, itinerary duration, duplicate submissions, and the original UI contract. A browser-level visual check still needs to be performed after installing Streamlit locally.

## Data and booking limitations

Flight and hotel values can be sample/estimated values depending on the configured tools. Google links open search results for location, photos, and reviews. This application does **not** make real reservations, confirm availability, or process payments. Always verify prices, dates, ratings, and booking conditions with the provider.

## Environment variables

Copy `.env.example` to `.env` only if you need optional API integrations. Add your own key locally. Never commit `.env` or share it publicly.
>>>>>>> origin/feature/sahil-day1-setup
