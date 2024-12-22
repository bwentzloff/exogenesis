from flask import Blueprint, jsonify, request
import json
from db import get_connection
import sqlite3

api_blueprint = Blueprint('api', __name__)

# Player APIs
@api_blueprint.route("/api/player/create", methods=["POST"])
def create_player():
    data = request.json
    name = data["name"]
    resources = {"energy": 50, "materials": 100}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO players (name, resources)
        VALUES (?, ?)
    """, (name, json.dumps(resources)))
    conn.commit()
    conn.close()

    return jsonify({"message": "Player created successfully!"})

@api_blueprint.route("/api/player/<int:player_id>", methods=["GET"])
def get_player_state(player_id):
    """Fetch player state by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row  # Ensures rows are returned as sqlite3.Row objects

    player = cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()
    conn.close()

    if player:
        # Convert to a dictionary for modification
        player_dict = dict(player)
        player_dict["resources"] = json.loads(player_dict["resources"])
        return jsonify(player_dict)

    return jsonify({"error": "Player not found"}), 404

# Task APIs
@api_blueprint.route("/api/tasks/<int:player_id>", methods=["GET"])
def get_tasks(player_id):
    conn = get_connection()
    cursor = conn.cursor()
    player = cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()

    tasks = [
        {"name": "Gather Energy", "required_traits": ["High Efficiency"], "reward": {"energy": 10}},
        {"name": "Build Storage", "required_traits": ["Structural Stability"], "reward": {"materials": 20}},
    ]

    conn.close()
    return jsonify({"tasks": tasks})

@api_blueprint.route("/api/task/assign", methods=["POST"])
def assign_task():
    data = request.json
    player_id = data["player_id"]
    task_name = data["task_name"]

    conn = get_connection()
    cursor = conn.cursor()

    # Deduct resources or check traits (logic can be added here)
    cursor.execute("""
        UPDATE players
        SET resources = JSON_SET(resources, '$.energy', JSON_EXTRACT(resources, '$.energy') - 10)
        WHERE id = ?
    """, (player_id,))

    conn.commit()
    conn.close()
    return jsonify({"message": f"Task {task_name} assigned successfully!"})

# Currency APIs
@api_blueprint.route("/api/currency/create_planetary", methods=["POST"])
def create_planetary_currency():
    data = request.json
    planet_id = data["planet_id"]
    currency_name = f"{data['planet_name']} Credits"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO currencies (name, type, owner_id, total_supply)
        VALUES (?, 'planetary', ?, 1000)
    """, (currency_name, planet_id))
    conn.commit()
    conn.close()

    return jsonify({"message": f"{currency_name} created successfully."})

@api_blueprint.route("/api/currency/buy", methods=["POST"])
def buy_currency():
    data = request.json
    buyer_id = data["buyer_id"]
    seller_id = data["seller_id"]
    currency_from_id = data["currency_from_id"]
    currency_to_id = data["currency_to_id"]
    amount = data["amount"]
    rate = data["rate"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO currency_exchange (buyer_id, seller_id, currency_from_id, currency_to_id, amount, rate, ticks_remaining)
        VALUES (?, ?, ?, ?, ?, ?, 5) -- Delay of 5 ticks
    """, (buyer_id, seller_id, currency_from_id, currency_to_id, amount, rate))
    conn.commit()
    conn.close()

    return jsonify({"message": "Currency exchange transaction initiated. It will complete in 5 ticks."})

@api_blueprint.route("/api/currency/exchange_rates", methods=["GET"])
def get_exchange_rates():
    conn = get_connection()
    cursor = conn.cursor()
    rates = cursor.execute("""
        SELECT id, name, exchange_rate FROM currencies
    """).fetchall()
    conn.close()

    return jsonify({"rates": rates})

@api_blueprint.route("/api/currency/notify", methods=["GET"])
def notify_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    notifications = cursor.execute("""
        SELECT * FROM currency_exchange
        WHERE ticks_remaining = 0
    """).fetchall()

    conn.close()
    return jsonify({"notifications": notifications})

@api_blueprint.route("/api/currency/clear_notifications", methods=["POST"])
def clear_notifications():
    player_id = request.json["player_id"]
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM notifications WHERE player_id = ?
    """, (player_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Notifications cleared."})

# Alliance APIs
@api_blueprint.route("/api/alliance/create", methods=["POST"])
def create_alliance():
    data = request.json
    name = data["name"]
    leader_id = data["leader_id"]
    description = data.get("description", "")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alliances (name, leader_id, description)
        VALUES (?, ?, ?)
    """, (name, leader_id, description))
    alliance_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO alliance_members (alliance_id, player_id, role)
        VALUES (?, ?, 'leader')
    """, (alliance_id, leader_id))

    conn.commit()
    conn.close()
    return jsonify({"message": "Alliance created successfully.", "alliance_id": alliance_id})

@api_blueprint.route("/api/alliance/members/<int:alliance_id>", methods=["GET"])
def get_alliance_members(alliance_id):
    conn = get_connection()
    cursor = conn.cursor()
    members = cursor.execute("""
        SELECT player_id, role FROM alliance_members WHERE alliance_id = ?
    """, (alliance_id,)).fetchall()
    conn.close()

    return jsonify({"members": members})
