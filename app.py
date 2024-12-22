from flask import Flask
from flask_login import LoginManager
from routes.auth import auth_blueprint
from routes.tasks import tasks_blueprint
from routes.map import map_blueprint
from db import initialize_database, seed_database

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a strong, secure key in production

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Redirect to login if authentication is required

# Register Blueprints
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(tasks_blueprint, url_prefix="/api")
app.register_blueprint(map_blueprint, url_prefix="/api/map")


# Initialize and seed the database
initialize_database()
seed_database()

# Root route to serve the main HTML page
@app.route("/")
def index():
    """Serve the main HTML page."""
    return app.send_static_file("index.html")

# Route to serve the favicon
@app.route("/favicon.ico")
def favicon():
    """Serve the favicon."""
    return app.send_static_file("favicon.ico")

if __name__ == "__main__":
    app.run(debug=True)
