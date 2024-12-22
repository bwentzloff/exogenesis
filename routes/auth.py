from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

auth_blueprint = Blueprint('auth', __name__)

# User Registration
@auth_blueprint.route('/api/auth/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    # Check if username already exists
    existing_user = cursor.execute("""
        SELECT * FROM users WHERE username = ?
    """, (username,)).fetchone()

    if existing_user:
        conn.close()
        return jsonify({"error": "Username already exists."}), 409

    # Insert new user
    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """, (username, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully!"}), 201

# User Login
@auth_blueprint.route('/api/auth/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch user from the database
    user = cursor.execute("""
        SELECT * FROM users WHERE username = ?
    """, (username,)).fetchone()

    conn.close()

    if user and check_password_hash(user["password"], password):
        # Set session
        session['user_id'] = user['id']
        return jsonify({"message": "Login successful!"}), 200

    return jsonify({"error": "Invalid username or password."}), 401

# User Logout
@auth_blueprint.route('/api/auth/logout', methods=['POST'])
def logout_user():
    session.clear()
    return jsonify({"message": "Logout successful!"}), 200

# Check Current Session
@auth_blueprint.route('/api/auth/session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({"user_id": user_id}), 200
    return jsonify({"error": "No active session."}), 401
