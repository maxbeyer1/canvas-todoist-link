import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CANVAS_ICS_URL = os.getenv('CANVAS_ICS_URL')
    FETCH_INTERVAL = int(os.getenv('FETCH_INTERVAL', 3600)
                         )  # Default to 1 hour if not set
    TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')

    COURSE_PROJECT_MAPPING = {
        # Course number (Canvas) : Project name (Todoist)
        'CCS_2024FA_MATH_230-1_ALL_SECTIONS': 'Math 230-1',
        '2024FA_ENGLISH_105-0_SEC20': 'English 105-0',
        '2024FA_ART_HIST_225-0_SEC1': 'Art History 225-0',
        '2024FA_COMP_SCI_213-0_SEC1': 'Comp Sci 213-0',
    }
