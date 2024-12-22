from flask import Flask, jsonify
from routes.tasks import tasks_blueprint
from routes.api import api_blueprint
from db import initialize_database, seed_database
import threading
import time

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)

# Initialize and seed the database on startup
initialize_database()
seed_database()

@app.route("/")
def index():
    """Serve the main HTML page."""
    return app.send_static_file("index.html")

@app.route("/favicon.ico")
def favicon():
    """Serve the favicon."""
    return app.send_static_file("favicon.ico")

if __name__ == "__main__":
    app.run(debug=True)
