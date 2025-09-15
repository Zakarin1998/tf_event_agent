import requests
from event_agent.config import EVENTBRITE_TOKEN

BASE_URL = "https://www.eventbriteapi.com/v3/"


def get_event(event_id: str):
    """Fetch a single event by ID from Eventbrite API"""
    url = f"{BASE_URL}events/{event_id}/"
    headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def search_events(query: str, location: str = "Torino", page: int = 1):
    """Search events with a query and location"""
    url = f"{BASE_URL}events/search/"
    headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}
    params = {
        "q": query,
        "location.address": location,
        "page": page
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()
