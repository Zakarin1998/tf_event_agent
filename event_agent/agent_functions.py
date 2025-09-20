"""Agent functions wrapper module."""
import re
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
from event_agent.eventbrite_wrapper import get_event, search_events
from event_agent.html_extractor import parse_html
# # # # # # #
# Entities  #
# # # # # # #


@dataclass
class Location:
    name: str
    address: Optional[str]
    city: str


@dataclass
class Guest:
    name: str
    role: Optional[str]


@dataclass
class Event:
    title: str
    date: str
    url: str
    location: Location
    guests: List[Guest]
    categories: List[str]
    description: Optional[str]


# # # # # # # # # # #
# Read/Write File   #
# # # # # # # # # # #
def load_json(path):
    """Load a JSON file and return its content."""
    with open(path, "r") as f:
        return json.load(f)


def write_json(path, content):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)
    return {"path": path, "status": "success"}


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"path": path, "status": "success"}


def parse_html_file(html_path):
    """Parse event.html and return project and dependencies info."""
    result = parse_html(html_path)
    return result


# # # # # # # # # # #
# Agent functions   #
# # # # # # # # # # #
def extract_event_id(url: str) -> str:
    """Extract Eventbrite ID from URL"""
    match = re.search(r'/(\d+)(?:/|$)', url)
    if not match:
        raise ValueError("ID evento non trovato nell'URL")
    return match.group(1)


def fetch_event_from_url(url: str) -> Event:
    """Fetch and parse an event from Eventbrite URL"""
    event_id = extract_event_id(url)
    data = get_event(event_id)
    return parse_event_json(data)


def parse_event_json(data: dict) -> Event:
    """Convert Eventbrite JSON to Event dataclass"""
    venue = data.get("venue", {})
    location = Location(
        name=venue.get("name", "Unknown"),
        address=venue.get("address", {}).get("localized_address_display"),
        city=venue.get("address", {}).get("city", "Torino")
    )

    # Eventbrite non sempre include guests → placeholder vuoto
    guests = []

    categories = [data.get("category", {}).get("name", "Generale")]

    return Event(
        title=data.get("name", {}).get("text"),
        date=data.get("start", {}).get("local"),
        url=data.get("url"),
        location=location,
        guests=guests,
        categories=categories,
        description=data.get("description", {}).get("text")
    )


def list_events_by_query(
        query: str,
        location: str = "Torino",
        page: int = 1
) -> List[Event]:
    """Search and return a list of Event objects"""
    raw = search_events(query, location, page)
    events = [parse_event_json(e) for e in raw.get("events", [])]
    return events



# travel_agent/agent_functions.py


# --- MOCK FUNCTIONS (simulano API reali) ---

def search_flights(origin: str, destination: str, date: str):
    """Restituisce un elenco di possibili trasporti (mock)"""
    return [
        {"company": "Ryanair", "mode": "Volo", "price": 60, "departure": "09:30", "arrival": "11:20"},
        {"company": "Trenitalia AV", "mode": "Treno Alta Velocità", "price": 45, "departure": "08:00", "arrival": "10:00"},
        {"company": "Italo", "mode": "Treno Alta Velocità", "price": 50, "departure": "10:15", "arrival": "12:15"},
    ]


def search_hotels(city: str, checkin: str, checkout: str):
    """Restituisce una lista di hotel disponibili (mock)"""
    return [
        {"name": "Hotel Centrale", "price_per_night": 90, "rating": 8.5, "distance_from_center": "0.5 km"},
        {"name": "B&B Panorama", "price_per_night": 60, "rating": 8.0, "distance_from_center": "1.2 km"},
        {"name": "Ostello Giovani", "price_per_night": 30, "rating": 7.5, "distance_from_center": "2 km"},
    ]


def search_events(city: str, date: str):
    """Restituisce eventi in città per quella data (mock)"""
    parsed_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    return [
        {"name": "Concerto Jazz", "time": "21:00", "location": "Teatro Comunale", "date": parsed_date},
        {"name": "Street Food Festival", "time": "Tutto il giorno", "location": "Piazza Duomo", "date": parsed_date},
        {"name": "Mostra d'Arte Moderna", "time": "10:00 - 18:00", "location": "Museo Civico", "date": parsed_date},
    ]


def get_weather_forecast(city: str, date: str):
    """Restituisce previsioni meteo (mock)"""
    return {
        "city": city,
        "date": date,
        "temperature": "22°C",
        "condition": "Soleggiato",
        "precipitation_probability": "10%"
    }
