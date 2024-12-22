from flask import Blueprint, jsonify, request
from db import get_connection
import json

tasks_blueprint = Blueprint('tasks', __name__)

# Fetch all tasks available to a player
@tasks_blueprint.route('/api/tasks/<int:player_id>', methods=['GET'])
def get_available_tasks(player_id):
    """Fetch all tasks available to the player based on their traits and resources."""
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch player data
    player = cursor.execute("""
        SELECT resources FROM players WHERE id = ?
    """, (player_id,)).fetchone()

    if not player:
        conn.close()
        return jsonify({"error": "Player not found."}), 404

    resources = json.loads(player["resources"])

    # Fetch all tasks
    tasks = cursor.execute("SELECT * FROM tasks").fetchall()

    # Filter tasks based on player resources
    available_tasks = []
    for task in tasks:
        task_resources = json.loads(task["required_resources"])
        if all(resources.get(resource, 0) >= amount for resource, amount in task_resources.items()):
            available_tasks.append({
                "id": task["id"],
                "name": task["name"],
                "description": task["description"],
                "required_resources": task_resources,
                "rewards": json.loads(task["rewards"]),
                "duration": task["duration"]
            })

    conn.close()
    return jsonify({"tasks": available_tasks})

# Assign a task to a player
@tasks_blueprint.route('/api/tasks/assign', methods=['POST'])
def assign_task():
    """Assign a task to the player, deduct resources, and start the task."""
    data = request.json
    player_id = data["player_id"]
    task_id = data["task_id"]

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch player resources
    player = cursor.execute("""
        SELECT resources FROM players WHERE id = ?
    """, (player_id,)).fetchone()

    if not player:
        conn.close()
        return jsonify({"error": "Player not found."}), 404

    resources = json.loads(player["resources"])

    # Fetch task details
    task = cursor.execute("""
        SELECT * FROM tasks WHERE id = ?
    """, (task_id,)).fetchone()

    if not task:
        conn.close()
        return jsonify({"error": "Task not found."}), 404

    task_resources = json.loads(task["required_resources"])

    # Check if player has sufficient resources
    if not all(resources.get(resource, 0) >= amount for resource, amount in task_resources.items()):
        conn.close()
        return jsonify({"error": "Insufficient resources for this task."}), 400

    # Deduct resources from player
    for resource, amount in task_resources.items():
        resources[resource] -= amount

    cursor.execute("""
        UPDATE players
        SET resources = ?
        WHERE id = ?
    """, (json.dumps(resources), player_id))

    # Start the task
    cursor.execute("""
        INSERT INTO active_tasks (player_id, task_id, ticks_remaining)
        VALUES (?, ?, ?)
    """, (player_id, task_id, task["duration"]))

    conn.commit()
    conn.close()

    return jsonify({"message": f"Task '{task['name']}' assigned successfully!"})

# Fetch active tasks for a player
@tasks_blueprint.route('/api/tasks/active/<int:player_id>', methods=['GET'])
def get_active_tasks(player_id):
    """Fetch all active tasks for a player."""
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch active tasks for the player
    active_tasks = cursor.execute("""
        SELECT at.id, t.name, at.ticks_remaining
        FROM active_tasks at
        JOIN tasks t ON at.task_id = t.id
        WHERE at.player_id = ?
    """, (player_id,)).fetchall()

    conn.close()
    return jsonify({"active_tasks": active_tasks})

# Complete tasks at the end of their duration
@tasks_blueprint.route('/api/tasks/complete', methods=['POST'])
def complete_tasks():
    """Complete tasks with 0 ticks remaining and grant rewards to the player."""
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch tasks that are ready to be completed
    completed_tasks = cursor.execute("""
        SELECT at.id as active_task_id, at.player_id, t.rewards
        FROM active_tasks at
        JOIN tasks t ON at.task_id = t.id
        WHERE at.ticks_remaining = 0
    """).fetchall()

    for task in completed_tasks:
        player_id = task["player_id"]
        rewards = json.loads(task["rewards"])

        # Fetch player resources
        player = cursor.execute("""
            SELECT resources FROM players WHERE id = ?
        """, (player_id,)).fetchone()

        resources = json.loads(player["resources"])

        # Grant rewards to the player
        for resource, amount in rewards.items():
            resources[resource] = resources.get(resource, 0) + amount

        cursor.execute("""
            UPDATE players
            SET resources = ?
            WHERE id = ?
        """, (json.dumps(resources), player_id))

        # Remove the completed task
        cursor.execute("""
            DELETE FROM active_tasks WHERE id = ?
        """, (task["active_task_id"],))

    conn.commit()
    conn.close()

    return jsonify({"message": "All completed tasks have been processed."})
