import sqlite3

DB_PATH = "game_state.db"

def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        amount INTEGER NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        room TEXT NOT NULL,
        ticks_remaining INTEGER NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY,
        message TEXT NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS celestial_bodies (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        explored BOOLEAN NOT NULL DEFAULT FALSE,
        resources TEXT
    );
    """)

    conn.commit()
    conn.close()

def seed_database():
    """Seed the database with default values."""
    conn = get_connection()
    cursor = conn.cursor()

    # Add default resources
    resources = [("energy", 75), ("materials", 60), ("data", 40)]
    for resource in resources:
        cursor.execute("""
        INSERT OR IGNORE INTO resources (name, amount) VALUES (?, ?)
        """, resource)

    # Add default celestial bodies
    celestial_bodies = [
        ("Home Moon", "moon", False, '{"energy": 10, "data": 5}'),
        ("Home Planet", "planet", False, '{"materials": 50, "energy": 20}')
    ]
    for body in celestial_bodies:
        cursor.execute("""
        INSERT OR IGNORE INTO celestial_bodies (name, type, explored, resources) VALUES (?, ?, ?, ?)
        """, body)

    conn.commit()
    conn.close()
