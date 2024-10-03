import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CANVAS_ICS_URL = os.getenv('CANVAS_ICS_URL')
    FETCH_INTERVAL = int(os.getenv('FETCH_INTERVAL', 3600)
                         )  # Default to 1 hour if not set
