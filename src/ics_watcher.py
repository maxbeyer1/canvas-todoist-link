from datetime import datetime
import requests
from icalendar import Calendar

from .config import Config


class ICSWatcher:
    def __init__(self):
        self.ics_url = Config.CANVAS_ICS_URL

    def fetch_ics_feed(self):
        try:
            response = requests.get(self.ics_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching ICS feed: {e}")
            return None

    def parse_ics_feed(self, ics_data):
        if not ics_data:
            return []

        cal = Calendar.from_ical(ics_data)
        events = []

        for component in cal.walk():
            if component.name == "VEVENT":
                event = {
                    'title': component.get('summary'),
                    'uid': component.get('uid'),
                    'date': component.get('dtstart').dt
                }
                events.append(event)

        return events

    def get_events(self):
        ics_data = self.fetch_ics_feed()
        return self.parse_ics_feed(ics_data)
