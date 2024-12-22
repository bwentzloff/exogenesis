import sqlite3

# Database file path
DATABASE_FILE = "game.db"

def initialize_database():
    """Initialize the SQLite database with the required schema."""
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Create players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            resources TEXT NOT NULL, -- JSON format: {"energy": 50, "materials": 100}
            tech_level INTEGER DEFAULT 0,
            location TEXT DEFAULT "Home Moon"
        )
    """)

    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            required_resources TEXT NOT NULL, -- JSON format: {"energy": 10, "materials": 5}
            rewards TEXT NOT NULL, -- JSON format: {"energy": 5, "materials": 10}
            duration INTEGER DEFAULT 1
        )
    """)

    # Create active tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_tasks (
            id INTEGER PRIMARY KEY,
            player_id INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            ticks_remaining INTEGER NOT NULL
        )
    """)

    # Create celestial bodies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS celestial_bodies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL, -- "moon", "planet", etc.
            resources TEXT NOT NULL, -- JSON format: {"energy": 20, "materials": 50}
            explored BOOLEAN DEFAULT 0
        )
    """)

    # Create currencies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS currencies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL, -- "planetary", "alliance", "government"
            owner_id INTEGER, -- Planet ID, Alliance ID, or Government ID
            exchange_rate REAL DEFAULT 1.0,
            total_supply REAL DEFAULT 1000
        )
    """)

    # Create currency exchange table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS currency_exchange (
            id INTEGER PRIMARY KEY,
            buyer_id INTEGER NOT NULL,
            seller_id INTEGER NOT NULL,
            currency_from_id INTEGER NOT NULL,
            currency_to_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            rate REAL NOT NULL,
            ticks_remaining INTEGER DEFAULT 5
        )
    """)

    # Create notifications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY,
            player_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create alliances table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alliances (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            leader_id INTEGER NOT NULL,
            description TEXT
        )
    """)

    # Create alliance members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alliance_members (
            id INTEGER PRIMARY KEY,
            alliance_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            role TEXT -- e.g., "leader", "member", "diplomat"
        )
    """)

    # Commit changes and close connection
    connection.commit()
    connection.close()
    print(f"Database initialized successfully at {DATABASE_FILE}")

if __name__ == "__main__":
    initialize_database()
