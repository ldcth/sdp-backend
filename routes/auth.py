from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from database.user import Users

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
bcrypt = Bcrypt()

@bp.post('/create')
def create_account():
    data = request.json
    user = Users()
    res = user.find_by_email(data["email"])
    if res:
        return jsonify({"message": "This email is already used!"}), 400
    
    user.name = data["name"]
    user.email = data["email"]
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    user.password = hashed_password
    user.role = 1
    user.save_to_db()
    return jsonify(user.__dict__), 200

@bp.post('/login')
def login():
    data = request.json
    user = Users()
    check = user.find_by_email(data["email"])
    if not check:
        return jsonify({"message": "Invalid email or password"}), 401
        
    is_valid = bcrypt.check_password_hash(user.password, data["password"])
    if not is_valid:
        return jsonify({"message": "Invalid email or password"}), 401
        
    access_token = create_access_token(
        identity=user.__dict__, expires_delta=timedelta(days=30))
    return jsonify({
        "user": user.__dict__,
        "access_token": access_token
    }), 200 