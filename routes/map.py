from flask import Blueprint, jsonify, request
from db import get_connection

map_blueprint = Blueprint('map', __name__)

# Fetch all celestial bodies for the galactic map
@map_blueprint.route('/api/map', methods=['GET'])
def get_celestial_bodies():
    """Fetch all celestial bodies for the galactic map."""
    conn = get_connection()
    cursor = conn.cursor()
    celestial_bodies = cursor.execute("""
        SELECT id, name, type, resources, explored
        FROM celestial_bodies
    """).fetchall()
    conn.close()

    # Format the resources field as JSON
    for body in celestial_bodies:
        body['resources'] = json.loads(body['resources'])

    return jsonify({"celestial_bodies": celestial_bodies})

# Mark a celestial body as explored
@map_blueprint.route('/api/map/explore', methods=['POST'])
def explore_celestial_body():
    """Mark a celestial body as explored."""
    data = request.json
    body_id = data.get('id')

    conn = get_connection()
    cursor = conn.cursor()

    # Check if the celestial body exists
    body = cursor.execute("""
        SELECT * FROM celestial_bodies WHERE id = ?
    """, (body_id,)).fetchone()

    if not body:
        conn.close()
        return jsonify({"error": "Celestial body not found."}), 404

    # Mark the celestial body as explored
    cursor.execute("""
        UPDATE celestial_bodies
        SET explored = 1
        WHERE id = ?
    """, (body_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"{body['name']} has been explored!"})

# Add a new celestial body
@map_blueprint.route('/api/map/add', methods=['POST'])
def add_celestial_body():
    """Add a new celestial body to the map."""
    data = request.json
    name = data.get('name')
    body_type = data.get('type')
    resources = json.dumps(data.get('resources', {}))
    explored = data.get('explored', False)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO celestial_bodies (name, type, resources, explored)
        VALUES (?, ?, ?, ?)
    """, (name, body_type, resources, explored))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Celestial body '{name}' added successfully!"})

# Fetch details of a specific celestial body
@map_blueprint.route('/api/map/body/<int:body_id>', methods=['GET'])
def get_celestial_body_details(body_id):
    """Fetch detailed information about a specific celestial body."""
    conn = get_connection()
    cursor = conn.cursor()
    body = cursor.execute("""
        SELECT * FROM celestial_bodies WHERE id = ?
    """, (body_id,)).fetchone()

    conn.close()
    if not body:
        return jsonify({"error": "Celestial body not found."}), 404

    body['resources'] = json.loads(body['resources'])
    return jsonify({"celestial_body": body})
