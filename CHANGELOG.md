# Changelog

All notable changes to this project will be documented in this file.

This project follows **Semantic Versioning** and uses **Conventional Commits** as a guideline for documenting changes.

---

## [0.1.0] – 2026-01-04

### Added
- Initial release of **MyStudyAgenda**, a desktop application for study planning
- Task management:
  - Create, edit, complete, and schedule tasks
  - Assign priorities to tasks
- Topic management:
  - Create and organize study topics
  - Associate tasks and notes with topics
- Notes management:
  - Create, edit, and delete notes
  - Notebook view for note editing
- Weekly planner view:
  - Visual representation of scheduled tasks
  - Navigation between weeks
- Pomodoro timer:
  - Configurable study and break durations
  - Timer reset and countdown functionality
- Graphical user interface built with **Kivy** and **KivyMD**
- SQLite persistence layer for tasks, topics, and notes

### Testing
- Unit tests for:
  - Model
  - DAO
  - Controller layers (using `unittest`)
- GUI tests for the View layer using:
  - `unittest` for structure and logic
  - `pytest` for improved compatibility with CI environments
- Headless UI testing configuration for CI environments

### CI/CD
- Continuous Integration pipeline with GitHub Actions:
  - Multi-platform testing (Linux, Windows, macOS)
  - Python 3.10, 3.11, 3.12 support
- Continuous Deployment pipeline:
  - Manual release triggered via Git tags
  - Package build using **Poetry**
  - Publication to **TestPyPI**
  - Automatic GitHub Release creation

### Documentation
- Project documentation covering:
  - Architecture
  - Validation and testing strategy
  - Release process
  - Licensing and versioning decisions

---

## Notes
This is the first public release of the project.  
Any future releases will expand functionality and test coverage and follow Semantic Versioning.
