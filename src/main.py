import time
import logging
from ics_watcher import ICSWatcher
from event_processor import EventProcessor
from config import Config


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    watcher = ICSWatcher()
    processor = EventProcessor()

    while True:
        try:
            print("\nFetching events...")
            events = watcher.get_events()
            print(f"Fetched {len(events)} events from ICS feed.")

            print("\nProcessing events...")
            new_assignments = processor.process_events(events)
            print(f"Processed {len(new_assignments)} new assignments:")
            for assignment in new_assignments:
                print(f"  - {assignment['title']} (Course: {
                      assignment['course_number']}, Due: {assignment['due_date']})")
                print(f"    Added to database with UID: {assignment['uid']}")

            print("\nChecking for pending assignments...")
            pending_assignments = processor.get_pending_assignments()
            print(f"Found {len(pending_assignments)} pending assignments:")
            for assignment in pending_assignments:
                uid, title, course_number, due_date, processed_date, _, sync_status = assignment
                print(f"  - {title} (Course: {course_number}, Due: {due_date})")
                print(f"    Status: {sync_status}, Processed on: {
                      processed_date}")

                # Simulate Todoist task creation
                print(f"    Simulating Todoist task creation for: {title}")
                success = True  # In a real scenario, this would depend on the Todoist API call

                if success:
                    processor.mark_assignment_synced(
                        uid, "fake_todoist_task_id_123")
                    print(
                        "    Marked as synced in database with Todoist task ID: fake_todoist_task_id_123")
                else:
                    processor.mark_assignment_failed(uid)
                    print("    Marked as failed in database")

            print(f"\nWaiting {
                  Config.FETCH_INTERVAL} seconds before next fetch...")
            time.sleep(Config.FETCH_INTERVAL)

        except Exception as e:
            logging.error("An error occurred in the main loop: %s", str(e))
            print(f"An error occurred. Check the log for details. Retrying in {
                  Config.FETCH_INTERVAL} seconds...")
            time.sleep(Config.FETCH_INTERVAL)


if __name__ == "__main__":
    main()
