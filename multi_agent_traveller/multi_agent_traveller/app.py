import streamlit as st
import sys
from pathlib import Path
from datetime import date, timedelta

# Ensure project root is on sys.path so agent/tool imports work
_PROJECT_DIR = Path(__file__).resolve().parent
if str(_PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(_PROJECT_DIR))

from agents.coordinator_agent import CoordinatorAgent
from utils.models import TripRequest

# =========================================================
# CONFIGURATION
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent
MAIN_FILE = PROJECT_DIR / "main.py"

st.set_page_config(
    page_title="TravelMate | Explore Beyond",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Real photography from Unsplash
HERO_IMAGE = (
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470"
    "?auto=format&fit=crop&w=2200&q=85"
)

# ─── Destination data grouped by category ───

CATEGORIES = {
    "ISLAND ESCAPE": {
        "icon": "🏝️",
        "description": "Sun-kissed shores and turquoise waters await",
        "color": "#0ea5a0",
        "places": [
            {
                "name": "Bali, Indonesia",
                "description": "Tropical escapes & island sunsets among ancient temples and lush rice terraces.",
                "image": (
                    "https://images.unsplash.com/photo-1537996194471-e657df975ab4"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Temple Tours", "Rice Terraces", "Surfing", "Spa & Wellness"],
                "best_time": "April – October",
                "avg_budget": "₹45,000",
            },
            {
                "name": "Switzerland, Europe",
                "description": "Alpine escapes with snow-capped mountains, crystal-clear lakes, scenic trains, and charming villages.",
                "image": ("https://images.unsplash.com/photo-1531366936337-7c912a4589a7?auto=format&fit=crop&w=900&q=80"),
                "highlights": ["Swiss Alps", "Lake Cruises", "Scenic Train Rides", "Mountain Hiking"],
                "best_time": "June – September; December – March for snow",
                "avg_budget": "₹1,50,000"
            },
             {
                "name": "Japan",
                "description": "Cultural journeys blending ancient shrines, peaceful gardens, neon-lit cities, and breathtaking cherry blossoms.",
                "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=900&q=80",
                "highlights": ["Mount Fuji", "Cherry Blossoms", "Temple Visits", "Traditional Cuisine"],
                "best_time": "March – May; October – November",
                "avg_budget": "₹1,00,000"
            },
             {
                "name": "Dubai, UAE",
                "description": "Modern city adventures featuring futuristic skyscrapers, golden deserts, luxury shopping, and vibrant nightlife.",
                "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=900&q=80",
                "highlights": ["Burj Khalifa", "Desert Safari", "Luxury Shopping", "Marina Cruises"],
                "best_time": "November – March",
                "avg_budget": "₹65,000"
            },
            {
                "name": "Maldives",
                "description": "Crystal-clear lagoons and overwater villas in a paradise archipelago.",
                "image": (
                    "https://images.unsplash.com/photo-1514282401047-d79a71a590e8"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Snorkeling", "Overwater Villas", "Sunset Cruises", "Diving"],
                "best_time": "November – April",
                "avg_budget": "₹1,20,000",
            },
             {
                "name": "Thailand",
                "description": "Tropical adventures with lively street markets, golden temples, tropical islands, and flavorful local cuisine.",
                "image": "https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=900&q=80",
                "highlights": ["Island Hopping", "Temple Tours", "Street Food", "Beach Adventures"],
                "best_time": "November – February",
                "avg_budget": "₹40,000"
            },
             {
                "name": "Paris, France",
                "description": "Romantic city escapes filled with iconic landmarks, charming cafés, world-class art, and elegant streets.",
                "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=900&q=80",
                "highlights": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise", "French Cafés"],
                "best_time": "April – June; September – October",
                "avg_budget": "₹1,20,000"
            },
            {
                "name": "Singapore",
                "description": "A vibrant urban getaway with futuristic gardens, waterfront skylines, cultural neighborhoods, and exciting attractions.",
                "image": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=900&q=80",
                "highlights": ["Gardens by the Bay", "Marina Bay Sands", "Sentosa Island", "Night Safari"],
                "best_time": "February – April",
                "avg_budget": "₹55,000"
            },
             {
                "name": "New Zealand",
                "description": "Outdoor escapes across dramatic fjords, emerald lakes, snow-capped peaks, and rolling countryside.",
                "image": "https://images.unsplash.com/photo-1469521669194-babb45599def?auto=format&fit=crop&w=900&q=80",
                "highlights": ["Milford Sound", "Lake Tekapo", "Mountain Hiking", "Adventure Sports"],
                "best_time": "December – March",
                "avg_budget": "₹1,80,000"
            },
            {
                "name": "Iceland, Europe",
                "description": "Arctic escapes featuring powerful waterfalls, volcanic landscapes, glaciers, and magical Northern Lights.",
                "image": "https://images.unsplash.com/photo-1476610182048-b716b8518aae?auto=format&fit=crop&w=900&q=80",
                "highlights": ["Northern Lights", "Glacier Adventures", "Waterfall Tours", "Geothermal Spas"],
                "best_time": "June – August; September – March for Northern Lights",
                "avg_budget": "₹1,50,000"
            },
            {
                "name": "Phuket, Thailand",
                "description": "Vibrant nightlife, stunning beaches and rich Thai culture.",
                "image": (
                    "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Beach Hopping", "Thai Cuisine", "Island Tours", "Night Markets"],
                "best_time": "November – February",
                "avg_budget": "₹35,000",
            },
        ],
    },
    "MOUNTAIN RETREAT": {
        "icon": "🏔️",
        "description": "Majestic peaks and crisp alpine air",
        "color": "#2d6a4f",
        "places": [
            {
                "name": "Swiss Alps",
                "description": "Mountain air & scenic adventures among snow-capped peaks and charming villages.",
                "image": (
                    "https://images.unsplash.com/photo-1531366936337-7c912a4589a7"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Skiing", "Hiking", "Scenic Trains", "Cheese & Chocolate Tours"],
                "best_time": "June – September / December – March",
                "avg_budget": "₹1,50,000",
            },
            {
                "name": "Manali, India",
                "description": "Snow-dusted valleys with adventure sports and serene mountain temples.",
                "image": (
                    "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Paragliding", "Rohtang Pass", "Old Manali", "River Rafting"],
                "best_time": "October – February / March – June",
                "avg_budget": "₹15,000",
            },
                        
            {
                "name": "Dolomites, Italy",
                "description": "Dramatic limestone peaks, alpine meadows, and peaceful mountain villages with breathtaking hiking trails.",
                "image": (
                    "https://images.unsplash.com/photo-1519681393784-d120267933ba"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Mountain Hiking", "Alpine Lakes", "Cable Cars", "Scenic Villages"],
                "best_time": "June – September / December – March",
                "avg_budget": "₹1,20,000",
            },
            {
                "name": "Sikkim, India",
                "description": "A peaceful Himalayan escape with snow-covered peaks, Buddhist monasteries, and spectacular mountain valleys.",
                "image": (
                    "https://images.unsplash.com/photo-1622308644420-b20142dc993c"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Kanchenjunga Views", "Monastery Tours", "Tsomgo Lake", "Mountain Drives"],
                "best_time": "March – May / October – November",
                "avg_budget": "₹20,000",
            },
            {
                "name": "Banff, Canada",
                "description": "A breathtaking mountain retreat with turquoise alpine lakes, towering peaks, evergreen forests, and cozy lodges.",
                "image": (
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgEdcNinz2g0GpgPCT2x-XZp3mmHSbg1a-w2cWdCrMKg&s=10"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Lake Louise", "Mountain Hiking", "Wildlife Watching", "Gondola Rides"],
                "best_time": "June – September / December – March",
                "avg_budget": "₹1,80,000",
            },
            {
                "name": "Swiss Jura, Switzerland",
                "description": "Quiet mountain escapes with forested ridges, rolling green hills, and charming countryside villages.",
                "image": (
                    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Forest Hiking", "Mountain Views", "Village Stays", "Nature Trails"],
                "best_time": "May – October",
                "avg_budget": "₹1,30,000",
            },
            {
                "name": "Gulmarg, India",
                "description": "A Himalayan paradise with snowy slopes, pine forests, alpine meadows, and spectacular mountain scenery.",
                "image": (
                    "https://images.unsplash.com/photo-1605649487212-47bdab064df7"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Gondola Rides", "Skiing", "Snowboarding", "Alpine Meadows"],
                "best_time": "December – March / May – September",
                "avg_budget": "₹18,000",
            },
            {
                "name": "Zermatt, Switzerland",
                "description": "An elegant alpine retreat beneath the iconic Matterhorn, featuring mountain railways and peaceful car-free streets.",
                "image": (
                    "https://images.unsplash.com/photo-1531366936337-7c912a4589a7"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Matterhorn Views", "Gornergrat Railway", "Skiing", "Alpine Hiking"],
                "best_time": "June – September / December – March",
                "avg_budget": "₹1,60,000",
            },
            {
                "name": "Queenstown, New Zealand",
                "description": "A scenic lakeside mountain getaway surrounded by dramatic peaks, vineyards, and adventure-filled valleys.",
                "image": (
                    "https://images.unsplash.com/photo-1469521669194-babb45599def"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Lake Wakatipu", "Mountain Gondola", "Hiking", "Adventure Sports"],
                "best_time": "December – February / June – August",
                "avg_budget": "₹1,70,000",
            },
            {
                "name": "Leh-Ladakh, India",
                "description": "A high-altitude Himalayan escape with rugged mountains, ancient monasteries, crystal-blue lakes, and winding roads.",
                "image": (
                    "https://images.unsplash.com/photo-1519681393784-d120267933ba"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Pangong Lake", "Nubra Valley", "Monastery Visits", "Mountain Road Trips"],
                "best_time": "May – September",
                "avg_budget": "₹25,000",
            },
            {
                "name": "Chamonix, France",
                "description": "A classic alpine retreat beneath Mont Blanc, with glacier panoramas, mountain cable cars, and picturesque chalets.",
                "image": (
                    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Mont Blanc Views", "Glacier Excursions", "Cable Cars", "Alpine Hiking"],
                "best_time": "June – September / December – March",
                "avg_budget": "₹1,40,000",
            },


            {
                "name": "Patagonia, Argentina",
                "description": "Untamed wilderness of glaciers, forests, and turquoise lakes.",
                "image": (
                    "https://images.unsplash.com/photo-1531761535209-180857e963b9"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Glacier Trekking", "Torres del Paine", "Wildlife", "Kayaking"],
                "best_time": "October – March",
                "avg_budget": "₹2,00,000",
            },
        ]
    },
    "COASTAL GETAWAY": {
        "icon": "🌊",
        "description": "Where the ocean meets unforgettable moments",
        "color": "#3a86c4",
        "places": [
            {
                "name": "Santorini, Greece",
                "description": "Whitewashed beauty by the Aegean Sea with legendary sunsets.",
                "image": (
                    "https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Oia Sunset", "Wine Tasting", "Caldera Cruise", "Greek Cuisine"],
                "best_time": "April – October",
                "avg_budget": "₹1,00,000",
            },
             {
                "name": "Langkawi, Malaysia",
                "description": "A tropical island escape with emerald rainforests, turquoise bays, sandy beaches, and spectacular coastal views.",
                "image": (
                    "https://images.unsplash.com/photo-1501785888041-af3ef285b470"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Island Hopping", "Sky Bridge", "Mangrove Tours", "Beach Sunsets"],
                "best_time": "November – April",
                "avg_budget": "₹45,000",
            },
            {
                "name": "Krabi, Thailand",
                "description": "A stunning seaside retreat featuring limestone cliffs, hidden lagoons, tropical beaches, and clear blue waters.",
                "image": (
                    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Railay Beach", "Four Islands Tour", "Kayaking", "Snorkeling"],
                "best_time": "November – April",
                "avg_budget": "₹40,000",
            },
            {
                "name": "Mauritius",
                "description": "A beautiful Indian Ocean escape with coral reefs, volcanic scenery, palm-lined shores, and peaceful lagoons.",
                "image": (
                    "https://images.unsplash.com/photo-1519046904884-53103b34b206"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Catamaran Cruises", "Coral Reef Diving", "Chamarel", "Beach Resorts"],
                "best_time": "May – December",
                "avg_budget": "₹85,000",
            },
            {
                "name": "Zanzibar, Tanzania",
                "description": "An exotic coastal escape blending white-sand beaches, turquoise waters, spice plantations, and historic island culture.",
                "image": (
                    "https://images.unsplash.com/photo-1544551763-46a013bb70d5"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Stone Town", "Dhow Sailing", "Snorkeling", "Spice Tours"],
                "best_time": "June – October / December – February",
                "avg_budget": "₹90,000",
            },
            {
                "name": "Algarve, Portugal",
                "description": "A sun-soaked European coastline with golden cliffs, sea caves, charming fishing towns, and hidden sandy coves.",
                "image": (
                    "https://images.unsplash.com/photo-1510414842594-a61c69b5ae57"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Benagil Cave", "Coastal Hiking", "Boat Tours", "Seafood Dining"],
                "best_time": "May – September",
                "avg_budget": "₹1,10,000",
            },
            {
                "name": "Pondicherry, India",
                "description": "A charming seaside getaway with French colonial streets, colorful cafés, tranquil promenades, and coastal sunsets.",
                "image": (
                    "https://images.unsplash.com/photo-1473116763249-2faaef81ccda"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Promenade Beach", "French Quarter", "Auroville", "Café Hopping"],
                "best_time": "October – March",
                "avg_budget": "₹12,000",
            },
            {
                "name": "Palawan, Philippines",
                "description": "A tropical paradise of dramatic limestone islands, hidden lagoons, turquoise seas, and pristine white beaches.",
                "image": (
                    "https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["El Nido Lagoons", "Island Hopping", "Kayaking", "Coral Reefs"],
                "best_time": "November – May",
                "avg_budget": "₹75,000",
            },
            {
                "name": "Kovalam, India",
                "description": "A relaxing beach destination with crescent-shaped shores, swaying palms, lighthouse views, and traditional wellness retreats.",
                "image": (
                    "https://images.unsplash.com/photo-1500375592092-40eb2168fd21"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Lighthouse Beach", "Ayurvedic Spas", "Surfing", "Seafood"],
                "best_time": "November – February",
                "avg_budget": "₹15,000",
            },
            {
                "name": "Goa, India",
                "description": "Golden beaches, vibrant nightlife and Portuguese-era charm.",
                "image": (
                    "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Beach Parties", "Water Sports", "Old Goa Churches", "Seafood"],
                "best_time": "November – February",
                "avg_budget": "₹12,000",
            },
            {
                "name": "Amalfi Coast, Italy",
                "description": "Dramatic cliffs, pastel villages and Mediterranean glamour.",
                "image": (
                    "https://images.unsplash.com/photo-1534308983496-4fabb1a015ee"
                    "?auto=format&fit=crop&w=900&q=80"
                ),
                "highlights": ["Positano Walk", "Limoncello Tasting", "Boat Tours", "Ravello Gardens"],
                "best_time": "May – September",
                "avg_budget": "₹1,30,000",
            },
        ],
    },
}

# ─── Session state defaults ───

if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = None
if "selected_place" not in st.session_state:
    st.session_state["selected_place"] = None


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap'
    );

    :root {
        --ink: #142d29;
        --green: #1f5748;
        --mint: #e9f2e9;
        --paper: #faf9f5;
        --muted: #718078;
        --gold: #d7aa65;
    }

    html {
        scroll-behavior: smooth;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1320px;
        padding: 1.4rem 2.2rem 4rem;
    }

    /* Navigation */

    .nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0 24px;
        animation: fadeDown 0.8s ease both;
    }

    .brand {
        font-size: 25px;
        font-weight: 700;
        letter-spacing: -1px;
        color: var(--ink);
    }

    .brand span {
        color: var(--green);
    }

    .nav-label {
        color: #65736a;
        font-size: 13px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Hero */

    .hero {
        position: relative;
        overflow: hidden;
        min-height: 470px;
        border-radius: 25px;
        background-image:
            linear-gradient(
                90deg,
                rgba(10, 31, 28, 0.79) 0%,
                rgba(10, 31, 28, 0.48) 46%,
                rgba(10, 31, 28, 0.06) 100%
            ),
            url("HERO_REPLACE");
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        padding: 50px;
        animation: heroReveal 1s ease both;
        box-shadow: 0 18px 55px rgba(26, 53, 43, 0.12);
    }

    .hero-content {
        max-width: 640px;
        animation: fadeUp 1s 0.2s ease both;
    }

    .eyebrow {
        display: inline-block;
        color: #fff1cf;
        border: 1px solid rgba(255,255,255,0.45);
        background: rgba(255,255,255,0.10);
        padding: 9px 15px;
        border-radius: 30px;
        font-size: 11px;
        letter-spacing: 2px;
        margin-bottom: 23px;
        backdrop-filter: blur(8px);
    }

    .hero h1 {
        font-family: 'Playfair Display', serif;
        font-size: clamp(42px, 5vw, 70px);
        line-height: 1.09;
        letter-spacing: -1.5px;
        color: white;
        margin: 0 0 20px;
        font-weight: 600;
    }

    .hero h1 em {
        color: #e9c78e;
        font-style: normal;
    }

    .hero p {
        color: rgba(255,255,255,0.88);
        font-size: 16px;
        line-height: 1.8;
        max-width: 470px;
        margin-bottom: 25px;
    }

    .hero-pill {
        display: inline-block;
        background: #fff;
        color: var(--ink);
        padding: 13px 19px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 700;
    }

    /* Section headings */

    .section {
        padding-top: 45px;
        animation: fadeUp 0.8s ease both;
    }

    .section-kicker {
        color: var(--green);
        font-size: 11px;
        letter-spacing: 2.5px;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 35px;
        line-height: 1.2;
        color: var(--ink);
        margin: 0 0 10px;
    }

    .section-desc {
        font-size: 14px;
        line-height: 1.8;
        color: var(--muted);
        margin-bottom: 22px;
    }

    /* Destination cards */

    .destination-card {
        position: relative;
        height: 250px;
        overflow: hidden;
        border-radius: 17px;
        background: #dce6dc;
        background-size: cover;
        background-position: center;
        margin-bottom: 8px;
        transition: transform 0.35s ease, box-shadow 0.35s ease;
        cursor: pointer;
    }

    .destination-card:hover {
        transform: translateY(-7px);
        box-shadow: 0 18px 35px rgba(20,45,41,0.18);
    }

    .destination-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            180deg,
            transparent 25%,
            rgba(8,26,22,0.85) 100%
        );
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 22px;
    }

    .destination-tag {
        color: #f4d9a8;
        font-size: 10px;
        letter-spacing: 2px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    .destination-name {
        color: white;
        font-family: 'Playfair Display', serif;
        font-size: 25px;
        margin-bottom: 5px;
    }

    .destination-desc {
        color: rgba(255,255,255,0.85);
        font-size: 12px;
    }

    /* Category tabs */

    .category-tab {
        background: white;
        border: 1.5px solid #e3e7df;
        border-radius: 16px;
        padding: 22px 20px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 130px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    .category-tab:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(20,45,41,0.12);
        border-color: var(--green);
    }

    .category-tab .cat-icon {
        font-size: 36px;
        margin-bottom: 4px;
    }

    .category-tab .cat-title {
        font-size: 14px;
        font-weight: 700;
        color: var(--ink);
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .category-tab .cat-desc {
        font-size: 11px;
        color: var(--muted);
        line-height: 1.5;
    }

    /* Place detail hero */

    .place-hero {
        position: relative;
        overflow: hidden;
        min-height: 340px;
        border-radius: 22px;
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: flex-end;
        padding: 35px;
        box-shadow: 0 18px 45px rgba(26, 53, 43, 0.14);
        animation: heroReveal 0.8s ease both;
    }

    .place-hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            180deg,
            transparent 30%,
            rgba(8, 26, 22, 0.88) 100%
        );
    }

    .place-hero-content {
        position: relative;
        z-index: 1;
    }

    .place-hero-content h1 {
        font-family: 'Playfair Display', serif;
        font-size: 44px;
        color: white;
        margin: 0 0 8px;
        font-weight: 600;
    }

    .place-hero-content p {
        color: rgba(255,255,255,0.9);
        font-size: 15px;
        line-height: 1.7;
        max-width: 550px;
    }

    /* Highlight chips */

    .highlight-chip {
        display: inline-block;
        background: var(--mint);
        color: var(--green);
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 12px;
        font-weight: 600;
        margin: 4px 4px 4px 0;
        letter-spacing: 0.5px;
    }

    /* Info cards */

    .info-card {
        background: white;
        border: 1px solid #e8ebe4;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    }

    .info-card .info-label {
        font-size: 11px;
        color: var(--muted);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .info-card .info-value {
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        color: var(--ink);
        font-weight: 600;
    }

    /* Breadcrumb */

    .breadcrumb {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: var(--muted);
        margin-bottom: 20px;
        animation: fadeDown 0.6s ease both;
    }

    .breadcrumb .sep {
        color: #c5cec6;
    }

    .breadcrumb .current {
        color: var(--ink);
        font-weight: 600;
    }

    /* Form */

    .form-panel {
        background: #ffffff;
        padding: 24px;
        border: 1px solid #e8ebe4;
        border-radius: 18px;
        box-shadow: 0 12px 35px rgba(27, 54, 44, 0.04);
    }

    .form-caption {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.7;
        margin-bottom: 15px;
    }

    .stTextInput label,
    .stNumberInput label,
    .stDateInput label,
    .stMultiSelect label {
        color: var(--ink) !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        border-radius: 10px !important;
        background: #fcfcfa !important;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: var(--green) !important;
        box-shadow: 0 0 0 2px rgba(31,87,72,0.08) !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background: var(--green) !important;
        color: white !important;
        border: 1px solid var(--green) !important;
        border-radius: 11px !important;
        min-height: 48px;
        font-weight: 700 !important;
        transition: all 0.25s ease;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background: #143e32 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(31,87,72,0.18);
    }

    /* Feature strip */

    .feature {
        background: var(--mint);
        border-radius: 14px;
        padding: 19px 15px;
        margin-top: 14px;
        min-height: 95px;
    }

    .feature-icon {
        font-size: 23px;
        margin-bottom: 9px;
    }

    .feature-title {
        font-size: 13px;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 5px;
    }

    .feature-desc {
        font-size: 11px;
        line-height: 1.6;
        color: #66796c;
    }

    .result-panel {
        background: #ffffff;
        border: 1px solid #e8ebe4;
        padding: 23px;
        border-radius: 15px;
        margin: 15px 0;
    }

    /* ─── Professional Trip Plan Output ─── */

    .trip-header {
        background: linear-gradient(135deg, #142d29 0%, #1f5748 50%, #2d6a4f 100%);
        border-radius: 20px;
        padding: 35px 40px;
        color: white;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        animation: fadeUp 0.6s ease both;
    }

    .trip-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        background: rgba(255,255,255,0.04);
        border-radius: 50%;
    }

    .trip-header::after {
        content: '';
        position: absolute;
        bottom: -60px; left: 30%;
        width: 300px; height: 300px;
        background: rgba(255,255,255,0.02);
        border-radius: 50%;
    }

    .trip-header .trip-route {
        font-family: 'Playfair Display', serif;
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .trip-header .trip-dates {
        font-size: 14px;
        color: rgba(255,255,255,0.75);
        margin-bottom: 16px;
    }

    .trip-header .trip-stats {
        display: flex;
        gap: 30px;
        flex-wrap: wrap;
    }

    .trip-header .trip-stat {
        text-align: center;
    }

    .trip-header .trip-stat .stat-value {
        font-size: 22px;
        font-weight: 700;
        color: #e9c78e;
    }

    .trip-header .trip-stat .stat-label {
        font-size: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.6);
        margin-top: 2px;
    }

    /* Section dividers inside results */

    .plan-section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 30px 0 16px;
        animation: fadeUp 0.5s ease both;
    }

    .plan-section-header .ps-icon {
        font-size: 24px;
    }

    .plan-section-header .ps-title {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        color: var(--ink);
        font-weight: 600;
    }

    .plan-section-header .ps-line {
        flex: 1;
        height: 1px;
        background: #e0e5dc;
        margin-left: 8px;
    }

    /* Flight cards */

    .flight-card {
        background: white;
        border: 1px solid #e8ebe4;
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
        animation: fadeUp 0.5s ease both;
    }

    .flight-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(20,45,41,0.1);
        border-color: var(--green);
    }

    .flight-card .fc-airline {
        font-weight: 700;
        font-size: 15px;
        color: var(--ink);
    }

    .flight-card .fc-route {
        font-size: 12px;
        color: var(--muted);
        margin-top: 3px;
    }

    .flight-card .fc-duration {
        background: var(--mint);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        color: var(--green);
    }

    .flight-card .fc-price {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        font-weight: 700;
        color: var(--green);
    }

    .flight-card .fc-badge {
        display: inline-block;
        background: #d7aa65;
        color: white;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 1px;
        padding: 3px 10px;
        border-radius: 12px;
        margin-left: 6px;
        text-transform: uppercase;
        vertical-align: middle;
    }

    /* Hotel cards */

    .hotel-card {
        background: white;
        border: 1px solid #e8ebe4;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
        animation: fadeUp 0.5s ease both;
    }

    .hotel-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(20,45,41,0.1);
        border-color: var(--green);
    }

    .hotel-card .hc-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 10px;
    }

    .hotel-card .hc-name {
        font-weight: 700;
        font-size: 16px;
        color: var(--ink);
    }

    .hotel-card .hc-rating {
        background: var(--green);
        color: white;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 700;
    }

    .hotel-card .hc-neighborhood {
        font-size: 12px;
        color: var(--muted);
        margin-bottom: 8px;
    }

    .hotel-card .hc-price {
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        font-weight: 700;
        color: var(--green);
    }

    .hotel-card .hc-price span {
        font-family: 'DM Sans', sans-serif;
        font-size: 12px;
        font-weight: 400;
        color: var(--muted);
    }

    /* Weather cards */

    .weather-row {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 10px;
    }

    .weather-card {
        flex: 1;
        min-width: 140px;
        background: white;
        border: 1px solid #e8ebe4;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeUp 0.5s ease both;
    }

    .weather-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 22px rgba(20,45,41,0.08);
    }

    .weather-card .wc-day {
        font-size: 11px;
        color: var(--muted);
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .weather-card .wc-icon {
        font-size: 32px;
        margin-bottom: 6px;
    }

    .weather-card .wc-summary {
        font-size: 13px;
        font-weight: 600;
        color: var(--ink);
        margin-bottom: 6px;
    }

    .weather-card .wc-temps {
        font-size: 12px;
        color: var(--muted);
    }

    .weather-card .wc-temps strong {
        color: var(--ink);
        font-size: 16px;
    }

    /* Itinerary timeline */

    .itinerary-day {
        position: relative;
        padding: 0 0 25px 35px;
        border-left: 2px solid #d6ddd8;
        margin-left: 12px;
        animation: fadeUp 0.5s ease both;
    }

    .itinerary-day:last-child {
        border-left: 2px solid transparent;
    }

    .itinerary-day::before {
        content: '';
        position: absolute;
        left: -8px; top: 3px;
        width: 14px; height: 14px;
        border-radius: 50%;
        background: var(--green);
        border: 3px solid var(--paper);
        box-shadow: 0 0 0 2px var(--green);
    }

    .itinerary-day .id-label {
        font-weight: 700;
        font-size: 14px;
        color: var(--green);
        margin-bottom: 3px;
    }

    .itinerary-day .id-date {
        font-size: 11px;
        color: var(--muted);
        margin-bottom: 10px;
    }

    .itinerary-day .id-activity {
        background: white;
        border: 1px solid #eaede7;
        border-radius: 10px;
        padding: 10px 15px;
        font-size: 13px;
        color: var(--ink);
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease;
    }

    .itinerary-day .id-activity:hover {
        background: var(--mint);
        border-color: var(--green);
    }

    .itinerary-day .id-activity .act-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--gold);
        flex-shrink: 0;
    }

    /* Trip summary footer */

    .trip-footer {
        background: linear-gradient(135deg, #f5f0e8 0%, #e9f2e9 100%);
        border-radius: 16px;
        padding: 25px 30px;
        margin-top: 20px;
        text-align: center;
        animation: fadeUp 0.6s ease both;
    }

    .trip-footer .tf-text {
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        color: var(--ink);
        margin-bottom: 6px;
    }

    .trip-footer .tf-sub {
        font-size: 13px;
        color: var(--muted);
    }

    .footer {
        border-top: 1px solid #e3e7df;
        margin-top: 55px;
        padding-top: 25px;
        color: #78837b;
        font-size: 12px;
        text-align: center;
        line-height: 1.9;
    }

    /* Back button styling */
    .back-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: transparent;
        border: 1.5px solid #d0d7d1;
        color: var(--ink);
        padding: 8px 18px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.25s ease;
        font-family: 'DM Sans', sans-serif;
        margin-bottom: 18px;
    }

    .back-btn:hover {
        border-color: var(--green);
        color: var(--green);
        background: var(--mint);
    }

    /* Animations */

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(22px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeDown {
        from { opacity: 0; transform: translateY(-12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes heroReveal {
        from { opacity: 0; transform: scale(0.985); }
        to { opacity: 1; transform: scale(1); }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }

    @media (max-width: 700px) {
        .block-container {
            padding: 1rem 1rem 3rem;
        }

        .hero {
            min-height: 420px;
            padding: 27px;
            border-radius: 18px;
        }

        .hero h1 {
            font-size: 43px;
        }

        .section-title {
            font-size: 29px;
        }

        .nav-label {
            font-size: 9px;
            letter-spacing: 1px;
        }
    }
    </style>
    """.replace("HERO_REPLACE", HERO_IMAGE),
    unsafe_allow_html=True,
)


# =========================================================
# NAVIGATION HEADER (shared across all pages)
# =========================================================

st.markdown(
    """
    <div class="nav">
        <div class="brand">travel<span>mate.</span></div>
        <div class="nav-label">Discover · Explore · Experience</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER: find a place dict by name
# =========================================================

def find_place(name):
    """Return (category_key, place_dict) for the given place name."""
    for cat_key, cat_data in CATEGORIES.items():
        for place in cat_data["places"]:
            if place["name"] == name:
                return cat_key, place
    return None, None


# =========================================================
# PAGE: HOME (Hero landing)
# =========================================================

def render_home():
    st.markdown(
        """
        <section class="hero">
            <div class="hero-content">
                <div class="eyebrow">YOUR NEXT CHAPTER STARTS HERE</div>
                <h1>Somewhere<br>between <em>here</em><br>and extraordinary.</h1>
                <p>
                    Your next unforgettable journey is waiting.
                    Discover beautiful destinations and create
                    a trip that feels uniquely yours.
                </p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # CTA button ─ "Your journey, thoughtfully planned"
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("✦  Your journey, thoughtfully planned", key="hero_cta", use_container_width=False):
        st.session_state["page"] = "explore"
        st.rerun()

    # Features strip
    st.markdown(
        """
        <div class="section">
            <div class="section-kicker">TRAVEL, YOUR WAY</div>
            <div class="section-title">Less planning stress. More wonder.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feature_columns = st.columns(4)

    features = [
        ("🧭", "Thoughtful routes", "Start with your origin and destination."),
        ("💰", "Budget conscious", "Plan around your travel budget."),
        ("🌿", "Your interests", "Choose the experiences you love."),
        ("✈️", "Ready to explore", "Turn your travel ideas into a plan."),
    ]

    for column, feature in zip(feature_columns, features):
        with column:
            st.markdown(
                f"""
                <div class="feature">
                    <div class="feature-icon">{feature[0]}</div>
                    <div class="feature-title">{feature[1]}</div>
                    <div class="feature-desc">{feature[2]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =========================================================
# PAGE: EXPLORE (Categories + Places)
# =========================================================

def render_explore():
    # Back button
    if st.button("← Back to Home", key="back_to_home"):
        st.session_state["page"] = "home"
        st.session_state["selected_category"] = None
        st.rerun()

    st.markdown(
        """
        <div class="section" style="padding-top:10px;">
            <div class="section-kicker">A LITTLE INSPIRATION</div>
            <div class="section-title">Places that stay with you.</div>
            <div class="section-desc">
                From quiet coastlines to mountain escapes,
                find the feeling you want to travel for.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Category selector tabs ───
    cat_keys = list(CATEGORIES.keys())
    cat_columns = st.columns(len(cat_keys) + 1)

    with cat_columns[0]:
        st.markdown(
            """
            <div class="category-tab">
                <div class="cat-icon">🌍</div>
                <div class="cat-title">ALL DESTINATIONS</div>
                <div class="cat-desc">Browse all options across every category</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Show All Places", key="cat_all", use_container_width=True):
            st.session_state["selected_category"] = None
            st.rerun()

    for col, cat_key in zip(cat_columns[1:], cat_keys):
        cat = CATEGORIES[cat_key]
        with col:
            st.markdown(
                f"""
                <div class="category-tab">
                    <div class="cat-icon">{cat["icon"]}</div>
                    <div class="cat-title">{cat_key}</div>
                    <div class="cat-desc">{len(cat["places"])} places · {cat["description"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                f"Browse {cat_key.title()}",
                key=f"cat_{cat_key}",
                use_container_width=True,
            ):
                st.session_state["selected_category"] = cat_key
                st.rerun()

    # ─── Show places for selected category or all categories ───
    selected_cat = st.session_state.get("selected_category")

    if selected_cat and selected_cat in CATEGORIES:
        cats_to_display = [selected_cat]
        if st.button("← Show All Categories", key="show_all_btn"):
            st.session_state["selected_category"] = None
            st.rerun()
    else:
        cats_to_display = cat_keys

    for cat_name in cats_to_display:
        cat_data = CATEGORIES[cat_name]
        st.markdown(
            f"""
            <div class="section" style="padding-top: 35px; padding-bottom: 12px;">
                <div class="section-kicker">{cat_name}</div>
                <div class="section-title">{cat_data["icon"]}  {cat_name.title()} Destinations <span style="font-size:20px; font-weight:normal; color:var(--muted);">({len(cat_data["places"])} places)</span></div>
                <div class="section-desc">{cat_data["description"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        places = cat_data["places"]
        row_size = 3
        for row_start in range(0, len(places), row_size):
            row_items = places[row_start : row_start + row_size]
            cols = st.columns(3)
            for col_idx, place in enumerate(row_items):
                with cols[col_idx]:
                    st.markdown(
                        f"""
                        <div class="destination-card"
                            style="background-image: url('{place["image"]}');">
                            <div class="destination-overlay">
                                <div class="destination-tag">{cat_name}</div>
                                <div class="destination-name">{place["name"]}</div>
                                <div class="destination-desc">{place["description"][:60]}…</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        f"Explore {place['name']}  →",
                        key=f"place_{cat_name}_{place['name']}_{row_start + col_idx}",
                        use_container_width=True,
                    ):
                        st.session_state["selected_place"] = place["name"]
                        st.session_state["page"] = "place_detail"
                        st.rerun()


# =========================================================
# PAGE: PLACE DETAIL + TRAVEL PLANNER
# =========================================================

def render_place_detail():
    place_name = st.session_state.get("selected_place")
    cat_key, place = find_place(place_name)

    if not place:
        st.error("Place not found. Going back.")
        st.session_state["page"] = "explore"
        st.rerun()
        return

    # Back button
    if st.button("← Back to Explore", key="back_to_explore"):
        st.session_state["page"] = "explore"
        st.session_state["selected_category"] = cat_key
        st.rerun()

    # Breadcrumb
    st.markdown(
        f"""
        <div class="breadcrumb">
            <span>Home</span>
            <span class="sep">›</span>
            <span>{cat_key.title()}</span>
            <span class="sep">›</span>
            <span class="current">{place["name"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Place hero banner
    st.markdown(
        f"""
        <div class="place-hero" style="background-image: url('{place["image"]}');">
            <div class="place-hero-overlay"></div>
            <div class="place-hero-content">
                <div class="destination-tag" style="margin-bottom:12px;">{cat_key}</div>
                <h1>{place["name"]}</h1>
                <p>{place["description"]}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Info cards row
    info_cols = st.columns(3)
    with info_cols[0]:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🗓️ Best Time to Visit</div>
                <div class="info-value">{place["best_time"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with info_cols[1]:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">💰 Avg. Budget</div>
                <div class="info-value">{place["avg_budget"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with info_cols[2]:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">📍 Category</div>
                <div class="info-value">{cat_key.title()}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Highlights
    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-kicker">HIGHLIGHTS</div>
        """,
        unsafe_allow_html=True,
    )
    chips_html = "".join(
        f'<span class="highlight-chip">{h}</span>' for h in place["highlights"]
    )
    st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)

    # ─── Travel Plan Form ───

    st.markdown(
        f"""
        <div class="section">
            <div class="section-kicker">YOUR ADVENTURE BEGINS</div>
            <div class="section-title">Plan your trip to {place["name"]}</div>
            <div class="section-desc">
                Tell us a little about your trip.
                Your travel planner will take it from here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("### ✈️ Create your travel plan")
        st.markdown(
            '<div class="form-caption">'
            'Add your details below to get started.'
            '</div>',
            unsafe_allow_html=True,
        )

        with st.form("travel_planner_form"):
            col1, col2 = st.columns(2)

            with col1:
                origin = st.text_input(
                    "📍 Starting location",
                    placeholder="e.g. Pune",
                )

            with col2:
                # Pre-fill destination from selected place
                destination = st.text_input(
                    "🌍 Where do you want to go?",
                    value=place["name"].split(",")[0],
                    placeholder="e.g. Goa",
                )

            col3, col4 = st.columns(2)

            with col3:
                start_date = st.date_input(
                    "🗓️ Departure date",
                    value=date.today() + timedelta(days=7),
                    min_value=date.today(),
                )

            with col4:
                end_date = st.date_input(
                    "🗓️ Return date",
                    value=date.today() + timedelta(days=12),
                    min_value=date.today(),
                )

            col5, col6 = st.columns(2)

            with col5:
                budget = st.number_input(
                    "💰 Total budget (₹)",
                    min_value=1,
                    value=15000,
                    step=1000,
                )

            with col6:
                travelers = st.number_input(
                    "👥 Number of travelers",
                    min_value=1,
                    max_value=50,
                    value=2,
                    step=1,
                )

            # Pre-select preferences based on place highlights
            all_preferences = [
                "Adventure",
                "Nature",
                "Beaches",
                "Historical Places",
                "Food",
                "Shopping",
                "Relaxation",
                "Culture",
            ]
            # Auto-suggest relevant preferences from highlights
            suggested = []
            highlight_lower = [h.lower() for h in place["highlights"]]
            for pref in all_preferences:
                if any(pref.lower() in hl or hl in pref.lower() for hl in highlight_lower):
                    suggested.append(pref)
            if not suggested:
                suggested = ["Nature"]

            preferences = st.multiselect(
                "✨ What would you love to experience?",
                all_preferences,
                default=suggested,
            )

            submitted = st.form_submit_button(
                "Plan My Trip  →",
                use_container_width=True,
            )

    # ─── Execute planner ───

    if submitted:
        if not origin.strip():
            st.error("Please enter your starting location.")

        elif not destination.strip():
            st.error("Please enter your destination.")

        elif start_date >= end_date:
            st.error("Your return date must be after your departure date.")

        else:
            st.markdown(
                """
                <div class="section">
                    <div class="section-kicker">MADE FOR YOU</div>
                    <div class="section-title">Your journey is taking shape.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            try:
                with st.spinner(
                    "🌍 Your travel planner is preparing your trip..."
                ):
                    request = TripRequest(
                        destination=destination.strip(),
                        origin=origin.strip(),
                        start_date=start_date.isoformat(),
                        end_date=end_date.isoformat(),
                        budget=float(budget),
                        travelers=travelers,
                        preferences=preferences,
                    )
                    coordinator = CoordinatorAgent()
                    plan = coordinator.run(request)

                # ─── Trip header ───
                num_days = (end_date - start_date).days
                best_flight = min(plan.flights, key=lambda f: f.price) if plan.flights else None
                best_hotel = min(plan.hotels, key=lambda h: h.price_per_night) if plan.hotels else None

                st.markdown(
                    f"""
                    <div class="trip-header">
                        <div class="trip-route">{origin.strip()}  ✈  {destination.strip()}</div>
                        <div class="trip-dates">🗓️ {start_date.strftime('%b %d, %Y')} — {end_date.strftime('%b %d, %Y')}</div>
                        <div class="trip-stats">
                            <div class="trip-stat">
                                <div class="stat-value">{num_days}</div>
                                <div class="stat-label">Days</div>
                            </div>
                            <div class="trip-stat">
                                <div class="stat-value">{travelers}</div>
                                <div class="stat-label">Travelers</div>
                            </div>
                            <div class="trip-stat">
                                <div class="stat-value">₹{budget:,.0f}</div>
                                <div class="stat-label">Budget</div>
                            </div>
                            <div class="trip-stat">
                                <div class="stat-value">{len(plan.itinerary)}</div>
                                <div class="stat-label">Days Planned</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ─── Flights section ───
                if plan.flights:
                    st.markdown(
                        """
                        <div class="plan-section-header">
                            <span class="ps-icon">✈️</span>
                            <span class="ps-title">Flight Options</span>
                            <span class="ps-line"></span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    sorted_flights = sorted(plan.flights, key=lambda f: f.price)
                    for i, f in enumerate(sorted_flights):
                        badge = '<span class="fc-badge">Best Price</span>' if i == 0 else ''
                        st.markdown(
                            f"""
                            <div class="flight-card">
                                <div>
                                    <div class="fc-airline">{f.airline} {badge}</div>
                                    <div class="fc-route">{f.departure} → {f.arrival}</div>
                                </div>
                                <div class="fc-duration">{f.duration_hours}h</div>
                                <div class="fc-price">₹{f.price:,.0f}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                # ─── Hotels section ───
                if plan.hotels:
                    st.markdown(
                        """
                        <div class="plan-section-header">
                            <span class="ps-icon">🏨</span>
                            <span class="ps-title">Recommended Hotels</span>
                            <span class="ps-line"></span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    hotel_cols = st.columns(min(len(plan.hotels), 3))
                    for col, h in zip(hotel_cols, plan.hotels):
                        stars = '★' * int(round(h.rating)) + '☆' * (5 - int(round(h.rating)))
                        with col:
                            st.markdown(
                                f"""
                                <div class="hotel-card">
                                    <div class="hc-top">
                                        <div class="hc-name">{h.name}</div>
                                        <div class="hc-rating">★ {h.rating}</div>
                                    </div>
                                    <div class="hc-neighborhood">📍 {h.neighborhood} · {stars}</div>
                                    <div class="hc-price">₹{h.price_per_night:,.0f} <span>/ night</span></div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                # ─── Weather section ───
                if plan.weather:
                    st.markdown(
                        """
                        <div class="plan-section-header">
                            <span class="ps-icon">🌤️</span>
                            <span class="ps-title">Weather Forecast</span>
                            <span class="ps-line"></span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    def weather_emoji(summary: str) -> str:
                        s = summary.lower()
                        if 'clear' in s or 'sunny' in s:
                            return '☀️'
                        elif 'mainly clear' in s:
                            return '🌤️'
                        elif 'partly' in s:
                            return '⛅'
                        elif 'overcast' in s:
                            return '☁️'
                        elif 'fog' in s:
                            return '🌫️'
                        elif 'drizzle' in s:
                            return '🌦️'
                        elif 'snow' in s or 'freezing' in s:
                            return '❄️'
                        elif 'thunder' in s or 'storm' in s:
                            return '⛈️'
                        elif 'rain' in s or 'shower' in s:
                            return '🌧️'
                        elif 'cloud' in s:
                            return '☁️'
                        return '🌤️'

                    # Show weather cards — up to 7 days, in rows of 3-4
                    display_weather = plan.weather[:7]
                    # Split into rows for clean layout
                    row_size = min(len(display_weather), 4)
                    for row_start in range(0, len(display_weather), row_size):
                        row_items = display_weather[row_start:row_start + row_size]
                        weather_cols = st.columns(len(row_items))
                        for col, w in zip(weather_cols, row_items):
                            icon = weather_emoji(w.summary)
                            with col:
                                st.html(
                                    f'<div class="weather-card">'
                                    f'<div class="wc-day">{w.date}</div>'
                                    f'<div class="wc-icon">{icon}</div>'
                                    f'<div class="wc-summary">{w.summary}</div>'
                                    f'<div class="wc-temps"><strong>{w.high_c}&deg;</strong> / {w.low_c}&deg;C</div>'
                                    f'</div>'
                                )

                # ─── Itinerary section ───
                if plan.itinerary:
                    st.markdown(
                        """
                        <div class="plan-section-header">
                            <span class="ps-icon">📋</span>
                            <span class="ps-title">Day-by-Day Itinerary</span>
                            <span class="ps-line"></span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    for day in plan.itinerary:
                        acts = ''.join(
                            f'<div class="id-activity"><span class="act-dot"></span>{act}</div>'
                            for act in day.activities
                        )
                        st.html(
                            f'<div class="itinerary-day">'
                            f'<div class="id-label">Day {day.day_number}</div>'
                            f'<div class="id-date">{day.date}</div>'
                            f'{acts}'
                            f'</div>'
                        )

                # ─── Trip footer ───
                st.markdown(
                    """
                    <div class="trip-footer">
                        <div class="tf-text">Your adventure awaits ✨</div>
                        <div class="tf-sub">This plan was generated by TravelMate's multi-agent system. Prices and availability may vary.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception as error:
                st.error(f"Unable to generate your travel plan: {error}")
                with st.expander("Technical details"):
                    import traceback
                    st.code(traceback.format_exc())


# =========================================================
# PAGE ROUTER
# =========================================================

page = st.session_state.get("page", "home")

if page == "home":
    render_home()
elif page == "explore":
    render_explore()
elif page == "place_detail":
    render_place_detail()
else:
    render_home()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        <div style="font-size:18px;font-weight:700;color:#214a3d;">
            travelmate.
        </div>
        Made for the journeys that become your favourite stories.<br>
        Travel thoughtfully. Explore endlessly.
    </div>
    """,
    unsafe_allow_html=True,
)