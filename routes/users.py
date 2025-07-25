from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils.auth import hash_password, check_password
from utils.validators import validate_user_data

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return {"error": "User not found"}, 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    is_valid, error = validate_user_data(data)
    if not is_valid:
        return {"error": error}, 400

    hashed_pw = hash_password(data['password'])
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (data['name'], data['email'], hashed_pw)
    )
    conn.commit()
    conn.close()
    return {"message": "User created"}, 201

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (data.get('name'), data.get('email'), user_id)
    )
    conn.commit()
    conn.close()
    return {"message": "User updated"}, 200

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": f"User {user_id} deleted"}, 200

@user_bp.route('/search')
def search_user():
    name = request.args.get('name')
    if not name:
        return {"error": "Name parameter is required"}, 400
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f'%{name}%',)).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if user and check_password(password, user['password']):
        return jsonify({"status": "success", "user_id": user['id']})
    return jsonify({"status": "failed"}), 401
