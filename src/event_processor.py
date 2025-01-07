import re
import logging

from .database import Database


class EventProcessor:
    def __init__(self):
        self.db = Database()
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def process_events(self, events):
        assignments = []
        for event in events:
            try:
                if self.is_assignment(event) and not self.db.event_exists(event['uid']):
                    assignment_data = self.extract_assignment_data(event)
                    if assignment_data:
                        self.db.add_event(assignment_data)
                        assignments.append(assignment_data)
                        logging.info("Processed new assignment: %s",
                                     assignment_data['title'])
                    else:
                        logging.warning(
                            "Failed to extract assignment data for event: %s", event['uid'])
            except Exception as e:
                logging.error("Error processing event %s: %s",
                              event['uid'], str(e))
        return assignments

    def is_assignment(self, event):
        return 'assignment' in event['uid'].lower()

    def extract_course_number(self, title):
        pattern = r'\[((?:CCS_)?\d{4}[A-Z]{2,3}_[A-Z_]+_\d+(?:-\d+)?(?:_SEC\d+(?:_AND_SEC\d+)?|_ALL_SECTIONS)?)\]'
        match = re.search(pattern, title)
        if match:
            return match.group(1)
        return None

    def extract_assignment_data(self, event):
        course_number = self.extract_course_number(event['title'])
        if not course_number:
            return None

        # Remove the course number (including brackets) from the title
        clean_title = re.sub(
            r'\s*\[' + re.escape(course_number) + r'\]\s*', '', event['title']).strip()

        return {
            'uid': event['uid'],
            'title': clean_title,
            'course_number': course_number,
            'due_date': event['date']
        }

    def get_pending_assignments(self):
        return self.db.get_pending_events()

    def mark_assignment_synced(self, uid, todoist_task_id):
        self.db.update_sync_status(uid, 'synced', todoist_task_id)

    def mark_assignment_failed(self, uid):
        self.db.update_sync_status(uid, 'failed')
