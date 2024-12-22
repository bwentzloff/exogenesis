# Exogenesis

## Overview
**Exogenesis** is a retro-futuristic, multiplayer tick-based game where players rediscover the lost art of life creation in alien worlds. Starting on a forgotten moon base, players evolve species, explore the galaxy, form alliances, trade resources, and tackle complex challenges in a shared universe.

---

## Features
- **Player Management**: Create and manage a player profile with unique resources and progress.
- **Task System**: Assign tasks to gather resources, build structures, and unlock new technologies.
- **Galactic Map**: Explore celestial bodies and unlock their hidden resources.
- **Currency System**: Each planet generates its own currency, with a galactic exchange for trade.
- **Multiplayer Alliances**: Form alliances, create shared currencies, and govern your group.
- **Dynamic Economy**: Engage in a player-driven economy with dynamic exchange rates.
- **Retro-Futuristic Aesthetic**: Inspired by the golden age of science fiction.

---

## Prerequisites
Before running this project, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- SQLite (pre-installed with Python)
- Flask

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/username/exogenesis.git
cd exogenesis
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Initialize the Database
```bash
python
>>> from db import initialize_database
>>> initialize_database()
>>> exit()
```

---

## Running the Application

### Start the Server
```bash
flask run
```

### Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## Directory Structure
```
/exogenesis/
├── app.py                    # Main application entry point
├── db/
│   ├── __init__.py           # Database connection utility
│   └── schema.sql            # Database schema definitions
├── routes/
│   ├── __init__.py           # Blueprint initialization
│   ├── api.py                # API endpoints for core game logic
│   ├── map.py                # API endpoints for galactic map functionality
│   ├── tasks.py              # API endpoints for task management
│   ├── auth.py               # API endpoints for user authentication
│   ├── index.py              # Routes for rendering HTML templates
├── static/
│   ├── css/
│   │   └── styles.css        # Main stylesheet for the frontend
│   ├── js/
│   │   └── script.js         # Main JavaScript for the frontend
│   ├── images/
│   │   ├── favicon.ico       # Favicon for the web app
│   │   └── background.webp   # Background image for the game interface
├── templates/
│   ├── index.html            # Main landing page template
│   ├── moon_base.html        # Moon Base interface template
│   ├── galactic_map.html     # Galactic Map interface template
│   ├── alliance_management.html # Alliance Management interface template
│   ├── marketplace.html      # Galactic Marketplace interface template
├── README.md                 # Documentation on how to run the project locally
├── requirements.txt          # Python dependencies
└── .gitignore                # Git ignore file
```

---

## Gameplay Instructions

### Start the Game
1. Create a new player profile.
2. Begin by managing your moon base and completing tasks to gather resources.
3. Explore the galactic map to discover celestial bodies and unlock their resources.
4. Form alliances, trade in the galactic marketplace, and evolve your species to new heights.

### Advanced Features
- **Currency Exchange**: Engage in interplanetary trade through the galactic marketplace.
- **Alliances**: Build collaborative groups and establish governance systems.
- **Evolving Species**: Adapt your species to thrive in the game’s challenges.

---

## Contribution Guidelines
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature name"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
Special thanks to all contributors and play-testers who helped shape **Exogenesis** into an exciting and engaging game. 🚀
