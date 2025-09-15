"""Agent functions wrapper module."""
import re
import json
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
