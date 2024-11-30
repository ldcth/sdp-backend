from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.user import Users

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.get('/users')
@jwt_required()
def admin_get_list_user():
    user = Users()
    current_user = get_jwt_identity()
    if current_user["role"] == 2:
        res = user.get_all_user()
        return jsonify(res), 200
    return jsonify({
        "message": "You don't have permission to do this action."
    }), 403 