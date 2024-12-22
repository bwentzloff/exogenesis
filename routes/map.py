from flask import Blueprint, jsonify, request
import sqlite3

map_blueprint = Blueprint("map", __name__)

DB_PATH = "game_state.db"

def get_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@map_blueprint.route("/", methods=["GET"])
def get_map_data():
    """Retrieve celestial body data for the universe map."""
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all celestial bodies from the database
    cursor.execute("SELECT id, name, type, explored, resources FROM celestial_bodies")
    celestial_bodies = [
        {
            "id": row["id"],
            "name": row["name"],
            "type": row["type"],
            "explored": bool(row["explored"]),
            "resources": eval(row["resources"]) if row["resources"] else {}
        }
        for row in cursor.fetchall()
    ]

    conn.close()

    return jsonify({"celestial_bodies": celestial_bodies})

@map_blueprint.route("/explore", methods=["POST"])
def explore_body():
    """Mark a celestial body as explored."""
    body_id = request.json.get("id")
    if not body_id:
        return jsonify({"error": "Body ID is required."}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch the celestial body by ID
    cursor.execute("SELECT id, name, explored FROM celestial_bodies WHERE id = ?", (body_id,))
    body = cursor.fetchone()
    if not body:
        conn.close()
        return jsonify({"error": "Celestial body not found."}), 404

    if body["explored"]:
        conn.close()
        return jsonify({"message": f"{body['name']} is already explored."}), 200

    # Mark the celestial body as explored
    cursor.execute("UPDATE celestial_bodies SET explored = 1 WHERE id = ?", (body_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"{body['name']} has been explored!"}), 200

@map_blueprint.route("/initialize", methods=["POST"])
def initialize_map():
    """Initialize or reset the celestial bodies in the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing celestial bodies
    cursor.execute("DELETE FROM celestial_bodies")

    # Add default celestial bodies
    default_bodies = [
        {"id": 1, "name": "Home Moon", "type": "moon", "explored": 1, "resources": '{"energy": 10, "data": 5}'},
        {"id": 2, "name": "Home Planet", "type": "planet", "explored": 0, "resources": '{"materials": 50, "energy": 20}'},
    ]
    for body in default_bodies:
        cursor.execute("""
            INSERT INTO celestial_bodies (id, name, type, explored, resources)
            VALUES (?, ?, ?, ?, ?)
        """, (body["id"], body["name"], body["type"], body["explored"], body["resources"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Celestial bodies initialized."}), 200
