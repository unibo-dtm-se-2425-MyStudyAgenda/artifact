# MyStudyAgenda
**MyStudyAgenda** is a desktop application designed to help students organize their academic life. Built with **Python** and the **Kivy/KivyMD** framework, it provides an interface for managing tasks, deadlines, and study schedules entirely on your local machine.

## Project Structure
The repository follows a standard Python project structure managed by **Poetry**:
```bash
artifact/
├── app/                        # Main application source code
│   ├── main.py                 # Application entry point
│   ├── model/                  # Data models and business logic classes
│   ├── view/                   # UI components (Kivy/KivyMD screens and widgets)
│   ├── controller/             # Bridge between UI and data logic
│   ├── db/                     # Data management and SQLite persistence
│   └── __init__.py             # Python package initialization
├── tests/                      # Unit and GUI test suites
├── .github/                    
│   └── workflows/              # GitHub Actions pipeline definitions
│       ├── check.yml           # CI: Runs automated tests on multiple OS and Python versions
│       └── deploy.yml          # CD: Automates builds and releases to TestPyPI
├── pyproject.toml              # Poetry configuration, dependencies, and project metadata
├── poetry.lock                 # Locked versions of all dependencies for reproducible builds
├── pytest.ini                  # Configuration for the pytest framework (markers and paths)
├── CHANGELOG.md                # Documentation of version history and release changes
├── LICENSE                     # Project licensing terms and legal permissions
├── README.md                   # Main project overview and installation guide
└── ...                         
```

## Installation
### From TestPyPi (recommended for users)
1. **Install from TestPyPi:**
    ```bash
    pip install -i https://test.pypi.org/simple/ mystudyagenda

2. **Run the application**:
    ```bash
    python -m MyStudyAgenda

### From GitHub (for developers)
1. **Clone the repository:**
    ```bash
    git clone https://github.com/unibo-dtm-se-2425-MyStudyAgenda
    cd artifact

2. **Install with poetry:**
    ```bash
    pip install poetry
    poetry install

3. **Run the application**:
    ```bash
    poetry run python -m app.main

## Quick Start Guide
* Tasks List: view, add, edit, or delete study tasks
* Planner: visualize your upcoming deadlines in a dedicated weekly planner view
* Notes: quickly take lecture notes directly on this application
* Pomodoro Timer: for rigorous time management while getting the work done

## How To Contribute
Contributions are welcome! To maintain code quality:
1. Create a `feature/` branch
2. Ensure all logic tests pass: `poetry run pytest -m "not ui"`
3. Open a **Pull Request** for maintainer review.

For detailed guidelines, see the **Developer Guide** in the project documentation.

## CI/CD Status
This project uses GitHub Actions for quality assurance:
- CI: Automatically tests the code on Ubuntu, Windows, and macOS for Python 3.10–3.12. *Note: GUI testing is currently supported on Linux via Xvfb.*
- CD: Automatically builds and deploys to TestPyPI upon version tagging.

## Authors
- **Anna Campagna** - [anna-campagna](https://github.com/annacampagna)

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
