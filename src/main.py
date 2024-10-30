import time
import logging

from .ics_watcher import ICSWatcher
from .event_processor import EventProcessor
from .todoist_creator import TodoistCreator
from .config import Config


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    watcher = ICSWatcher()
    processor = EventProcessor()
    todoist = TodoistCreator(Config.TODOIST_API_TOKEN)

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

            print("\nCreating Todoist tasks...")
            created_task_ids = todoist.create_tasks_from_assignments(
                new_assignments)
            print(f"Created {len(created_task_ids)} Todoist tasks.")

            print("\nUpdating assignment sync status...")
            for assignment, task_id in zip(new_assignments, created_task_ids):
                if task_id:
                    processor.mark_assignment_synced(
                        assignment['uid'], task_id)
                    print(
                        f"  - Marked assignment {assignment['uid']} as synced with Todoist task {task_id}")
                else:
                    processor.mark_assignment_failed(assignment['uid'])
                    print(
                        f"  - Marked assignment {assignment['uid']} as failed to sync")

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
