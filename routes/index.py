from flask import Blueprint, jsonify, request, send_from_directory

index_blueprint = Blueprint("index", __name__, static_folder="../static")

@index_blueprint.route("/")
def serve_index():
    """Serve the main HTML page."""
    return send_from_directory(index_blueprint.static_folder, "index.html")

@index_blueprint.route("/favicon.ico")
def serve_favicon():
    """Serve the favicon."""
    return send_from_directory(index_blueprint.static_folder, "favicon.ico")

@index_blueprint.route("/static/<path:filename>")
def serve_static(filename):
    """Serve static files like CSS, JS, and images."""
    return send_from_directory(index_blueprint.static_folder, filename)
