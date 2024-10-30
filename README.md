# Canvas to Todoist Integration

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Python application that synchronizes Canvas assignments with Todoist tasks. This integration automatically fetches assignments from Canvas's ICS feed and creates corresponding tasks in Todoist, organizing them by course projects.

## 🌟 Features

- **Real-time Synchronization**: Continuously monitors Canvas calendar feed for new assignments
- **Smart Course Mapping**: Automatically maps Canvas courses to Todoist projects
- **Persistent Storage**: SQLite database to track sync status and prevent duplicates
- **Robust Error Handling**: Comprehensive logging and error recovery mechanisms
- **Flexible Configuration**: Environment-based configuration for easy deployment

## 🛠 Technology Stack

- **Python 3.8+**: Core programming language
- **SQLite**: Local database for event tracking
- **icalendar**: ICS feed parsing
- **Todoist API**: Task creation and management
- **Docker**: Containerization (optional)

## 📋 Prerequisites

- Python 3.8 or higher
- Todoist Premium account (for API access)
- Canvas calendar feed URL ([instructions to obtain](https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-view-the-Calendar-iCal-feed-to-subscribe-to-an-external/ta-p/617607))
- Docker (optional, for containerized deployment)

## 🚀 Installation

### Standard Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/canvas-todoist-sync.git
cd canvas-todoist-sync
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
CANVAS_ICS_URL=your_canvas_ics_url
TODOIST_API_TOKEN=your_todoist_api_token
FETCH_INTERVAL=3600  # Optional: defaults to 1 hour
```

### Docker Installation

1. Build the Docker image:

```bash
docker build -t canvas-todoist-sync .
```

2. Run the container:

```bash
docker run -d \
  --name canvas-todoist-sync \
  -e CANVAS_ICS_URL=your_canvas_ics_url \
  -e TODOIST_API_TOKEN=your_todoist_api_token \
  canvas-todoist-sync
```

#### With Docker-Compose

1. Build the container:

```bash
docker-compose build
```

2. Start the container:

```bash
docker-compose up -d
```

_[Makefile](Makefile) contains aliases to these commands for quick access_

## 🔧 Configuration

The application uses a configuration system defined in `config.py`. Key configurations include:

- Course to Project mapping in `COURSE_PROJECT_MAPPING`
- Environment variables for API tokens and URLs
- Configurable fetch interval

## 💡 Architecture

The project follows a modular architecture with clear separation of concerns:

- **ICSWatcher**: Handles Canvas calendar feed monitoring
- **EventProcessor**: Processes and filters assignment events
- **TodoistCreator**: Manages Todoist task creation
- **Database**: Provides persistent storage and tracking

### Data Flow

1. `ICSWatcher` fetches and parses the Canvas ICS feed
2. `EventProcessor` filters assignments and extracts relevant data
3. `Database` tracks processed events and their sync status
4. `TodoistCreator` creates tasks in mapped Todoist projects

## 📝 Technical Details

### Smart Course Detection

The application uses regex pattern matching to extract course numbers from assignment titles:

```python
pattern = r'$$((?:CCS_)?\d{4}[A-Z]{2,3}_[A-Z_]+_\d+(?:-\d+)?(?:_SEC\d+|_ALL_SECTIONS)?)$$'
```

### Error Handling

Comprehensive error handling ensures reliability:

- Connection error recovery
- Duplicate event prevention
- Failed sync tracking and retry capability

### Database Schema

```sql
CREATE TABLE IF NOT EXISTS events (
    uid TEXT PRIMARY KEY,
    title TEXT,
    course_number TEXT,
    due_date TEXT,
    processed_date TEXT,
    todoist_task_id TEXT,
    sync_status TEXT
)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Future Improvements

- [ ] Add support for assignment details and descriptions
- [ ] Add web interface for configuration
- [ ] Support for multiple Canvas calendars
- [ ] Task priority mapping

## 🔍 Project Motivation

This project was born from the need to streamline academic task management. As a student using both Canvas LMS and Todoist, I found myself manually copying assignments between platforms. This automation solution not only saves time but also ensures no assignments are missed.

The implementation showcases modern Python development practices including:

- Context managers for database connections
- Environment-based configuration
- Modular architecture
- Comprehensive logging
- Docker containerization
