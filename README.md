# 1. Project Title
**StressMate: Daily Wellness Companion**[cite: 22]

# 2. Project Description
**Brief Explanation of the System:**[cite: 22]
StressMate is an interactive desktop application designed to help users track their daily stress levels, reflect on their emotions through journaling, and receive actionable coping strategies tailored to their current mental state. 

**The Problem the System Addresses:**[cite: 22]
With the increasing demands of academic and professional life, many individuals experience burnout and anxiety without knowing how to pause or manage it. StressMate addresses the lack of accessible, immediate mental health tracking by providing an organized space to log feelings and offering instant grounding techniques (like the 4-7-8 breathing method or micro-tasks) to intercept extreme stress before it escalates.

# 3. Project Objectives
* To provide an intuitive and private desktop interface for daily stress logging and emotional reflection[cite: 22].
* To offer immediate, actionable advice and micro-tasks dynamically tailored to the user's specific stress tier (Green, Yellow, Orange, Red)[cite: 22].
* To maintain a secure database of user accounts and their emotional history, allowing users to look back and manage their well-being over time[cite: 22].

# 4. Features
* **Secure User Authentication:** A robust login and registration system featuring strict password validation (minimum length, uppercase, and numerical requirements) and secure SHA-256 password hashing[cite: 22].
* **Interactive Stress Logging:** Users can categorize their current stress into four color-coded tiers and add personal reflection notes to record their daily mental state[cite: 22].
* **History Management (CRUD):** Users can seamlessly view, update, and delete their past stress logs in a structured data table[cite: 22].
* **Coping & Support Resources:** Dedicated informative modules broken down into Physical, Emotional, and Spiritual help, providing specific grounding techniques and actionable advice[cite: 22].
* **Inspirational Quotes Album:** An interactive image gallery providing users with uplifting quotes and visual encouragement[cite: 22].

# 5. Technologies Used
* **Programming Language:** Python 3[cite: 22]
* **GUI Framework/Library:** PyQt6 (for building the modern, multi-screen graphical user interface)[cite: 22]
* **Database:** SQLite (via the built-in `sqlite3` module for local, lightweight database management)[cite: 22]
* **Other Important Libraries/Tools:**[cite: 22]
  * `hashlib`: For secure password hashing.
  * `re` (RegEx): For validating email formats and strict password rules.
  * `dataclasses`: For structuring clean, object-oriented domain models.
  * `os`: For dynamic and safe asset file path routing.

# 6. Project Structure
**Important Folders and Files:**[cite: 22]
* `/assets/`
* `/database/`
  * `database.py`
* `/features/`
  * `/authentication/`
  * `/tracker/`
* `main.py`
* `style.qss`

**Purpose of Each Major File or Folder:**[cite: 22]
* **`/assets/`**: Stores all static media resources, including the application logo, background images, overview infographics, and the quotes image gallery.
* **`/database/database.py`**: Encapsulates the SQLite connection logic and automatically executes the schema creation for the `users` and `stress_logs` tables.
* **`/features/`**: The core directory utilizing a layered Object-Oriented Programming (OOP) architecture. It is divided into `authentication` (handling logins/signups) and `tracker` (handling the main dashboard, CRUD operations, and support tabs).
  * Inside each feature, the code is cleanly separated into `model.py` (data structures), `repository.py` (database queries), `service.py` (business logic and validation), and `view.py` (PyQt6 UI rendering).
* **`main.py`**: The central entry point and orchestrator of the application. It initializes the database, connects the services, and uses a `QStackedWidget` to manage screen transitions.
* **`style.qss`**: The global stylesheet file that applies unified CSS-like styling (colors, fonts, borders) across all PyQt widgets in the application.