from flask import Blueprint, request, jsonify
import sqlite3

tasks_blueprint = Blueprint("tasks", __name__)

DB_PATH = "game_state.db"

def get_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@tasks_blueprint.route("/assign_task", methods=["POST"])
def assign_task():
    """Assign a task."""
    conn = get_connection()
    cursor = conn.cursor()

    # Extract data from the request
    task_name = request.json.get("task")
    room = request.json.get("room")
    ticks_required = request.json.get("ticks_required", 1)

    if not task_name or not room:
        conn.close()
        return jsonify({"error": "Task name and room are required."}), 400

    # Deduct resources (example logic, customize as needed)
    cursor.execute("SELECT amount FROM resources WHERE name = 'energy'")
    energy = cursor.fetchone()["amount"]
    if energy < 10:  # Example cost
        conn.close()
        return jsonify({"error": "Not enough energy to assign the task."}), 400

    cursor.execute("UPDATE resources SET amount = amount - 10 WHERE name = 'energy'")

    # Add the task to the tasks table
    cursor.execute("""
        INSERT INTO tasks (name, room, ticks_remaining)
        VALUES (?, ?, ?)
    """, (task_name, room, ticks_required))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Task '{task_name}' assigned to {room} for {ticks_required} ticks."}), 201

@tasks_blueprint.route("/clear_alerts", methods=["POST"])
def clear_alerts():
    """Clear all alerts."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()

    return jsonify({"message": "All alerts cleared!"}), 200

@tasks_blueprint.route("/tasks", methods=["GET"])
def get_tasks():
    """Get all active tasks."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, room, ticks_remaining FROM tasks")
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({"tasks": tasks})

@tasks_blueprint.route("/update_ticks", methods=["POST"])
def update_ticks():
    """Update task ticks (process a game tick)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET ticks_remaining = ticks_remaining - 1
        WHERE ticks_remaining > 0
    """)

    cursor.execute("""
        DELETE FROM tasks
        WHERE ticks_remaining <= 0
    """)

    conn.commit()
    conn.close()

    return jsonify({"message": "Task ticks updated."}), 200

@tasks_blueprint.route("/initialize_tasks", methods=["POST"])
def initialize_tasks():
    """Initialize or reset tasks in the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing tasks
    cursor.execute("DELETE FROM tasks")

    # Add default tasks (example tasks, customize as needed)
    default_tasks = [
        {"name": "Repair Comms Hub", "room": "Control Room", "ticks_remaining": 5},
        {"name": "Organize Storage", "room": "Storage Room", "ticks_remaining": 3},
    ]
    for task in default_tasks:
        cursor.execute("""
            INSERT INTO tasks (name, room, ticks_remaining)
            VALUES (?, ?, ?)
        """, (task["name"], task["room"], task["ticks_remaining"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Tasks initialized."}), 200

@tasks_blueprint.route("/state", methods=["GET"])
def get_game_state():
    """Retrieve the current game state."""
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch resources
    cursor.execute("SELECT name, amount FROM resources")
    resources = {row["name"]: row["amount"] for row in cursor.fetchall()}

    # Fetch tasks
    cursor.execute("SELECT name, room, ticks_remaining FROM tasks")
    tasks = [dict(row) for row in cursor.fetchall()]

    # Fetch alerts
    cursor.execute("SELECT message FROM alerts")
    alerts = [row["message"] for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        "resources": resources,
        "tasks": tasks,
        "alerts": alerts
    })
