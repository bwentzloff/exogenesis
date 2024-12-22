from flask import Blueprint, jsonify, request
import sqlite3
import threading
import time

tasks_blueprint = Blueprint("tasks", __name__)

DB_PATH = "game_state.db"
TICK_INTERVAL = 10

TASKS_DATA = {
    "Repair Comms Hub": {"costs": {"materials": 20}, "prerequisites": []},
    "Upgrade Antennas": {"costs": {"materials": 50}, "prerequisites": ["Repair Comms Hub"]},
    "Genetic Experiment": {"costs": {"data": 15}, "prerequisites": []},
    "Organize Storage": {"costs": {"materials": 10}, "prerequisites": []},
    "Send Signal": {"costs": {"energy": 10}, "prerequisites": []},
    "Harvest Solar Energy": {"costs": {}, "prerequisites": [], "generates": {"energy": 20}},
}

def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def process_tick():
    """Process a game tick."""
    while True:
        time.sleep(TICK_INTERVAL)
        conn = get_connection()
        cursor = conn.cursor()

        # Decrement ticks_remaining for tasks
        cursor.execute("UPDATE tasks SET ticks_remaining = ticks_remaining - 1 WHERE ticks_remaining > 0")

        # Remove completed tasks and apply effects
        cursor.execute("SELECT * FROM tasks WHERE ticks_remaining <= 0")
        completed_tasks = cursor.fetchall()
        for task in completed_tasks:
            if task["name"] == "Harvest Solar Energy":
                cursor.execute("UPDATE resources SET amount = amount + 20 WHERE name = 'energy'")
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task["id"],))

        # Add alerts for low resources
        cursor.execute("SELECT name, amount FROM resources")
        for row in cursor.fetchall():
            if row["amount"] < 20:
                alert_message = f"Warning: {row['name'].capitalize()} levels are critically low!"
                cursor.execute("INSERT OR IGNORE INTO alerts (message) VALUES (?)", (alert_message,))

        conn.commit()
        conn.close()

# Start the tick thread
tick_thread = threading.Thread(target=process_tick, daemon=True)
tick_thread.start()

@tasks_blueprint.route("/api/assign_task", methods=["POST"])
def assign_task():
    """Assign a task."""
    conn = get_connection()
    cursor = conn.cursor()

    task_name = request.json.get("task")
    room = request.json.get("room")
    ticks_required = request.json.get("ticks_required", 1)

    if not task_name or not room:
        return jsonify({"error": "Task name and room are required."}), 400

    if task_name not in TASKS_DATA:
        return jsonify({"error": "Invalid task name."}), 400

    task_data = TASKS_DATA[task_name]
    prerequisites = task_data["prerequisites"]

    # Check prerequisites
    for prereq in prerequisites:
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE name = ?", (prereq,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": f"Prerequisite '{prereq}' not completed."}), 400

    # Check resource costs
    for resource, cost in task_data["costs"].items():
        cursor.execute("SELECT amount FROM resources WHERE name = ?", (resource,))
        current_amount = cursor.fetchone()
        if not current_amount or current_amount["amount"] < cost:
            return jsonify({"error": f"Not enough {resource} to start task."}), 400

    # Deduct resources
    for resource, cost in task_data["costs"].items():
        cursor.execute("UPDATE resources SET amount = amount - ? WHERE name = ?", (cost, resource))

    # Add task to database
    cursor.execute(
        "INSERT INTO tasks (name, room, ticks_remaining) VALUES (?, ?, ?)",
        (task_name, room, ticks_required),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Task assigned successfully."}), 201

@tasks_blueprint.route("/api/clear_alerts", methods=["POST"])
def clear_alerts():
    """Clear all alerts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()
    return jsonify({"message": "All alerts cleared."}), 200
