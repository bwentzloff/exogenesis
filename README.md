
# Exogenesis: A Retro-Futuristic Tick-Based Game

## Overview
Exogenesis is a retro-futuristic tick-based game that allows players to manage resources, assign tasks, and explore a universe of celestial bodies. Built using Flask for the backend and SQLite for persistent storage, this game is designed to evolve with modular gameplay elements and enhancements.

---

## Features
- **Resource Management**: Track and manage resources like energy, materials, and data.
- **Task System**: Assign tasks, manage progress, and receive alerts.
- **Persistent Game State**: All data is stored in SQLite for reliability.
- **Interactive Universe Map**: Explore celestial bodies and unlock new gameplay elements.

---

## Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd exogenesis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize the Database
Run the database initialization script:
```bash
python db.py
```

### 4. Run the Application
Start the Flask development server:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

---

## Project Structure
- **`app.py`**: Main entry point for the Flask application.
- **`routes/`**: Contains modular Flask blueprints for API endpoints.
- **`static/`**: Static assets including CSS and JavaScript files.
- **`templates/`**: HTML templates for rendering the frontend.
- **`game_state.db`**: SQLite database file for persistent storage.

---

## Instructions for Checking into GitHub

### 1. Initialize a Git Repository
If not already initialized, run:
```bash
git init
```

### 2. Add All Files to the Repository
```bash
git add .
```

### 3. Commit Changes
```bash
git commit -m "Initial commit: Added Exogenesis game code"
```

### 4. Create a New Repository on GitHub
Go to [GitHub](https://github.com) and create a new repository.

### 5. Add Remote Repository
```bash
git remote add origin <your-repo-url>
```

### 6. Push to GitHub
```bash
git branch -M main
git push -u origin main
```

---

## Contributing
Feel free to fork the repository, submit issues, or create pull requests to suggest enhancements.

---

## License
MIT License
