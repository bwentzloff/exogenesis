from flask import Flask
from routes.api import api_blueprint
from routes.map import map_blueprint
from routes.tasks import tasks_blueprint
from routes.auth import auth_blueprint
from routes.index import index_blueprint
from db import initialize_database

# Initialize Flask app
app = Flask(__name__)

# Set secret key for session management
app.secret_key = 'your_secret_key'

# Register blueprints
app.register_blueprint(api_blueprint)
app.register_blueprint(map_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(index_blueprint)

# Initialize the database
with app.app_context():
    initialize_database()

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
