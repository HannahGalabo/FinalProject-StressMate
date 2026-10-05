# StressMate: Stress Tracker

## Project Description
StressMate is an interactive application designed to help users track their daily stress levels, reflect on their emotions through journaling, and receive actionable coping strategies tailored to their current mental state. 

With the increasing demands of academic and professional life, many individuals experience burnout and anxiety without knowing how to pause or manage it. StressMate provides an organized space to log feelings and offering instant grounding techniques (like the 4-7-8 breathing method or micro-tasks) to intercept extreme stress before it escalates.

## Project Objectives
* To provide daily stress logging and emotional reflection.
* To offer actionable advice and micro-tasks dynamically tailored to the user's specific stress tier (Green, Yellow, Orange, Red).
* To maintain a secure database of user accounts and their emotional history, allowing users to look back and manage their well-being over time.

## Features
* **Secure User Authentication:** A robust login and registration system featuring strict password validation (minimum length, uppercase, and numerical requirements) and secure SHA-256 password hashing.
* **Interactive Stress Logging:** Users can categorize their current stress into four color-coded tiers and add personal reflection notes to record their daily mental state.
* **History Management (CRUD):** Users can seamlessly view, update, and delete their past stress logs in a structured data table.
* **Coping & Support Resources:** Dedicated informative modules broken down into Physical, Emotional, and Spiritual help, providing specific grounding techniques and actionable advice.
* **Inspirational Quotes Album:** An interactive image gallery providing users with uplifting quotes and visual encouragement.

## Technologies Used
* **Programming Language:** Python 3
* **GUI Framework:** PyQt6
* **Database:** SQLite (via the built-in `sqlite3` module)
* **Other Important Libraries:**
  * `hashlib`: For secure password hashing.
  * `re` (RegEx): For validating email formats and strict password rules.
  * `dataclasses`: For structuring clean, object-oriented domain models.
  * `os`: For dynamic and safe asset file path routing.

## Project Structure
* **`/assets/`**: Stores all static media resources, including the application logo, background images, overview infographics, and the quotes image gallery.
* **`/database/`**: Contains `database.py`, which encapsulates the SQLite connection logic and automatically executes the schema creation for the `users` and `stress_logs` tables.
* **`/features/`**: The core directory utilizing a layered Object-Oriented Programming (OOP) architecture. It is divided into two main domains: `authentication` and `tracker`.
  * Inside each feature, the code is cleanly separated into `model.py` (data structures), `repository.py` (database queries), `service.py` (business logic and validation), and `view.py` (PyQt6 UI rendering).
* **`main.py`**: The central entry point and orchestrator of the application. It initializes the database, connects the services, and uses a `QStackedWidget` to manage screen transitions.
* **`style.qss`**: The global stylesheet file that applies unified CSS-like styling (colors, fonts, borders) across all PyQt widgets in the application.