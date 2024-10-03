import time

from ics_watcher import ICSWatcher
from config import Config


def main():
    watcher = ICSWatcher()

    while True:
        print("Fetching events...")
        events = watcher.get_events()

        for event in events:
            print(f"Title: {event['title']}")
            print(f"UID: {event['uid']}")
            print(f"Date: {event['date']}")
            print("---")

        print(f"Waiting {Config.FETCH_INTERVAL} seconds before next fetch...")
        time.sleep(Config.FETCH_INTERVAL)


if __name__ == "__main__":
    main()
