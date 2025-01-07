from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List
import logging
import os
import yaml
from dotenv import load_dotenv

# pylint: disable=invalid-name


class ConfigurationError(Exception):
    """Raised when there are configuration-related errors."""


@dataclass
class Config:
    """Configuration management for the Canvas-Todoist integration."""
    CANVAS_ICS_URL: str = field(init=False)
    TODOIST_API_TOKEN: str = field(init=False)
    FETCH_INTERVAL: int = field(init=False)
    COURSE_PROJECT_MAPPING: Dict[str, str] = field(init=False)
    DEFAULT_PROJECT: str = field(init=False)
    course_config: Dict = field(init=False, default_factory=dict)

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __post_init__(self):
        """Initialize configuration after instance creation."""
        self._load_configuration()

    def _load_configuration(self) -> None:
        """Load all configuration from environment and YAML files."""
        # Load environment variables
        load_dotenv()

        # Set required environment variables
        self.CANVAS_ICS_URL = self._get_required_env('CANVAS_ICS_URL')
        self.TODOIST_API_TOKEN = self._get_required_env('TODOIST_API_TOKEN')

        # Set optional environment variables with defaults
        self.FETCH_INTERVAL = int(os.getenv('FETCH_INTERVAL', '3600'))

        # Load course mappings from YAML
        self.course_config = self._load_course_mappings()

        # Set course mappings and other configurations
        self.COURSE_PROJECT_MAPPING = self.course_config.get('courses', {})
        self.DEFAULT_PROJECT = self.course_config.get(
            'default_project', 'Uncategorized')

    def _get_required_env(self, var_name: str) -> str:
        """Get a required environment variable or raise an error."""
        value = os.getenv(var_name)
        if not value:
            raise ConfigurationError(f"Required environment variable '{
                                     var_name}' is not set")
        return value

    def _load_course_mappings(self) -> Dict:
        """Load course mappings from the YAML file."""
        # Look for courses.yml in several locations
        possible_paths = [
            Path("courses.yml"),  # Root directory
            Path("config/courses.yml"),  # Config directory
            Path(__file__).parent.parent / "courses.yml",  # Project root
        ]

        for path in possible_paths:
            if path.is_file():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return yaml.safe_load(f) or {}
                except yaml.YAMLError as e:
                    raise ConfigurationError(
                        f"Error parsing courses.yml: {e}") from e
                except Exception as e:
                    raise ConfigurationError(
                        f"Error reading courses.yml: {e}") from e

        # If no file is found, return empty config but log a warning
        logging.warning(
            "No courses.yml file found. Using empty course mappings.")
        return {}

    def reload_configuration(self) -> None:
        """Reload configuration files."""
        self._load_configuration()

    def get_project_name(self, course_number: str) -> str:
        """Get the Todoist project name for a given course number."""
        return self.COURSE_PROJECT_MAPPING.get(course_number, self.DEFAULT_PROJECT)

    @property
    def course_patterns(self) -> List[Dict]:
        """Get the course number patterns from configuration."""
        return self.course_config.get('course_patterns', [])
