from flask import Blueprint, jsonify, request
import sqlite3

map_blueprint = Blueprint("map", __name__)

DB_PATH = "game_state.db"

def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@map_blueprint.route("/api/map", methods=["GET"])
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

@map_blueprint.route("/api/explore", methods=["POST"])
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

@map_blueprint.route("/api/initialize_map", methods=["POST"])
def initialize_map():
    """Initialize or reset celestial bodies in the database."""
    celestial_bodies = [
        {"name": "Home Moon", "type": "moon", "explored": False, "resources": '{"energy": 10, "data": 5}'},
        {"name": "Home Planet", "type": "planet", "explored": False, "resources": '{"materials": 50, "energy": 20}'},
    ]

    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM celestial_bodies")

    # Add default celestial bodies
    for body in celestial_bodies:
        cursor.execute(
            "INSERT INTO celestial_bodies (name, type, explored, resources) VALUES (?, ?, ?, ?)",
            (body["name"], body["type"], body["explored"], body["resources"]),
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "Celestial bodies initialized."}), 200
