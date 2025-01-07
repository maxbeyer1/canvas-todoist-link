from todoist_api_python.api import TodoistAPI

from .config import Config


class TodoistCreator:
    def __init__(self, api_token):
        self.api = TodoistAPI(api_token)
        self.projects = {}
        self.config = Config()
        self.fetch_projects()

    def fetch_projects(self):
        try:
            all_projects = self.api.get_projects()
            course_project_mapping = self.config.COURSE_PROJECT_MAPPING

            for project in all_projects:
                if project.name in course_project_mapping.values():
                    self.projects[project.name] = project.id
        except Exception as error:
            print(f"Error fetching Todoist projects: {error}")

    def get_project_id(self, course_number):
        project_name = self.config.get_project_name(course_number)

        return self.projects.get(project_name)

    def create_task(self, title, due, course_number):
        project_id = self.get_project_id(course_number)
        if not project_id:
            print(f"No matching project found for course number: {
                  course_number}")
            return None

        try:
            task = self.api.add_task(
                content=title,
                project_id=project_id,
                due_datetime=due.isoformat() if due else None
            )
            print(f"Task created: {task.content} (ID: {task.id})")
            return task.id
        except Exception as error:
            print(f"Error creating Todoist task: {error}")
            return None

    def create_tasks_from_assignments(self, assignments):
        created_task_ids = []
        for assignment in assignments:
            task_id = self.create_task(
                title=assignment['title'],
                due=assignment['due_date'],
                course_number=assignment['course_number']
            )
            if task_id:
                created_task_ids.append(task_id)
        return created_task_ids
