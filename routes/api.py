from flask import Blueprint, jsonify, request
import sqlite3

api_blueprint = Blueprint("api", __name__)

DB_PATH = "game_state.db"

def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@api_blueprint.route("/api/state", methods=["GET"])
def get_game_state():
    """Retrieve the current game state."""
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch resources
    cursor.execute("SELECT name, amount FROM resources")
    resources = {row["name"]: row["amount"] for row in cursor.fetchall()}

    # Fetch tasks
    cursor.execute("SELECT id, name, room, ticks_remaining FROM tasks")
    tasks = [dict(row) for row in cursor.fetchall()]

    # Fetch alerts
    cursor.execute("SELECT message FROM alerts")
    alerts = [row["message"] for row in cursor.fetchall()]

    conn.close()

    return jsonify({"resources": resources, "tasks": tasks, "alerts": alerts})

@api_blueprint.route("/api/map", methods=["GET"])
def get_map_data():
    """Retrieve celestial bodies for the known universe map."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, type, explored, resources FROM celestial_bodies")
    celestial_bodies = [
        {
            "id": row["id"],
            "name": row["name"],
            "type": row["type"],
            "explored": bool(row["explored"]),
            "resources": row["resources"],
        }
        for row in cursor.fetchall()
    ]

    conn.close()

    return jsonify({"celestial_bodies": celestial_bodies})

@api_blueprint.route("/api/explore", methods=["POST"])
def explore_body():
    """Mark a celestial body as explored."""
    body_id = request.json.get("id")

    if not body_id:
        return jsonify({"error": "Body ID is required."}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM celestial_bodies WHERE id = ? AND explored = 0", (body_id,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return jsonify({"error": "Celestial body not found or already explored."}), 404

    cursor.execute("UPDATE celestial_bodies SET explored = 1 WHERE id = ?", (body_id,))
    conn.commit()

    conn.close()

    return jsonify({"message": f"{result['name']} has been explored!"}), 200
