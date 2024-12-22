from flask import Flask, jsonify, request, render_template, send_from_directory
import threading
import time
import random
import json
import os

app = Flask(__name__)

# Global game state
GAME_STATE_FILE = "game_state.json"
game_state = {
    "resources": {
        "energy": 75,
        "materials": 60,
        "data": 40
    },
    "tasks": [],
    "alerts": []
}

# Tasks data with costs and prerequisites
TASKS_DATA = {
    "Repair Comms Hub": {"costs": {"materials": 20}, "prerequisites": []},
    "Upgrade Antennas": {"costs": {"materials": 50}, "prerequisites": ["Repair Comms Hub"]},
    "Genetic Experiment": {"costs": {"data": 15}, "prerequisites": []},
    "Organize Storage": {"costs": {"materials": 10}, "prerequisites": []},
    "Send Signal": {"costs": {"energy": 10}, "prerequisites": []}
}

# Tick interval in seconds
tick_interval = 10

def save_game_state():
    """Save the current game state to a file."""
    with open(GAME_STATE_FILE, "w") as file:
        json.dump(game_state, file)

def load_game_state():
    """Load the game state from a file."""
    global game_state
    try:
        with open(GAME_STATE_FILE, "r") as file:
            game_state = json.load(file)
    except FileNotFoundError:
        save_game_state()

# Load the game state on startup
load_game_state()

def process_tick():
    """Process a game tick."""
    global game_state
    while True:
        time.sleep(tick_interval)

        # Update tasks
        for task in game_state["tasks"]:
            if task["ticks_remaining"] > 0:
                task["ticks_remaining"] -= 1

                # Lower failure chance
                if random.random() < 0.02:  # 2% chance
                    game_state["alerts"].append(f"Task {task['name']} failed!")
                    game_state["tasks"].remove(task)

        # Remove completed tasks
        completed_tasks = [task for task in game_state["tasks"] if task["ticks_remaining"] == 0]
        for task in completed_tasks:
            if task["name"] == "Repair Comms Hub":
                game_state["resources"]["energy"] += 10

        game_state["tasks"] = [task for task in game_state["tasks"] if task["ticks_remaining"] > 0]

        # Example alerts
        if game_state["resources"]["energy"] < 20:
            if "Low energy levels!" not in game_state["alerts"]:
                game_state["alerts"].append("Low energy levels!")

        # Save the updated game state
        save_game_state()

# Start the tick system in a background thread
tick_thread = threading.Thread(target=process_tick, daemon=True)
tick_thread.start()

@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    """Serve the favicon."""
    return send_from_directory(
        os.path.join(app.root_path, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )

@app.route("/api/state", methods=["GET"])
def get_game_state():
    """API endpoint to get the current game state."""
    return jsonify(game_state)

@app.route("/api/assign_task", methods=["POST"])
def assign_task():
    """API endpoint to assign a new task."""
    global game_state
    task_name = request.json.get("task")
    room = request.json.get("room")
    ticks_required = request.json.get("ticks_required", 1)

    if task_name not in TASKS_DATA:
        return jsonify({"error": "Invalid task name."}), 400

    task_data = TASKS_DATA[task_name]
    prerequisites = task_data["prerequisites"]

    # Check prerequisites
    if any(prereq not in [t["name"] for t in game_state["tasks"]] for prereq in prerequisites):
        return jsonify({"error": "Prerequisites not met."}), 400

    # Check resource costs
    for resource, cost in task_data["costs"].items():
        if game_state["resources"].get(resource, 0) < cost:
            return jsonify({"error": f"Not enough {resource} to start task."}), 400

    # Deduct resources
    for resource, cost in task_data["costs"].items():
        game_state["resources"][resource] -= cost

    # Add task to game state
    game_state["tasks"].append({
        "name": task_name,
        "room": room,
        "ticks_remaining": ticks_required
    })

    save_game_state()
    return jsonify({"message": "Task added successfully!"}), 201

@app.route("/api/clear_alerts", methods=["POST"])
def clear_alerts():
    """API endpoint to clear all alerts."""
    global game_state
    game_state["alerts"] = []
    save_game_state()
    return jsonify({"message": "Alerts cleared!"})

if __name__ == "__main__":
    app.run(debug=True)
