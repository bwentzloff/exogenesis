-- Players table
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    resources TEXT NOT NULL, -- JSON format: {"energy": 50, "materials": 100}
    tech_level INTEGER DEFAULT 0,
    location TEXT DEFAULT "Home Moon"
);

-- Tasks table
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    required_traits TEXT, -- JSON array of traits required
    rewards TEXT, -- JSON format: {"energy": 10, "materials": 5}
    duration INTEGER DEFAULT 1 -- Duration in ticks
);

-- Currencies table
CREATE TABLE currencies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- "planetary", "alliance", "government"
    owner_id INTEGER, -- Planet ID, Alliance ID, or Government ID
    exchange_rate REAL DEFAULT 1.0, -- Relative to Galactic Standard
    total_supply REAL DEFAULT 1000
);

-- Currency balances table
CREATE TABLE currency_balances (
    id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL,
    currency_id INTEGER NOT NULL,
    amount REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS active_tasks (
    id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    ticks_remaining INTEGER NOT NULL
);


-- Currency exchange table
CREATE TABLE currency_exchange (
    id INTEGER PRIMARY KEY,
    buyer_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    currency_from_id INTEGER NOT NULL,
    currency_to_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    rate REAL NOT NULL,
    ticks_remaining INTEGER DEFAULT 5 -- Delay for interstellar transactions
);

-- Alliances table
CREATE TABLE alliances (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    leader_id INTEGER NOT NULL,
    description TEXT
);

-- Alliance members table
CREATE TABLE alliance_members (
    id INTEGER PRIMARY KEY,
    alliance_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    role TEXT -- e.g., "leader", "member", "diplomat"
);

-- Celestial bodies table
CREATE TABLE celestial_bodies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- "moon", "planet", etc.
    resources TEXT -- JSON format: {"energy": 20, "materials": 50}
);

-- Notifications table
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Votes table for governments and alliances
CREATE TABLE votes (
    id INTEGER PRIMARY KEY,
    legislation_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    vote TEXT NOT NULL -- "yes" or "no"
);

-- Governments table
CREATE TABLE governments (
    id INTEGER PRIMARY KEY,
    alliance_id INTEGER NOT NULL,
    type TEXT NOT NULL, -- "democracy", "monarchy", etc.
    constitution TEXT -- JSON defining the rules and roles
);

-- Legislation table
CREATE TABLE legislation (
    id INTEGER PRIMARY KEY,
    government_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT -- "proposed", "enacted", "rejected"
);
