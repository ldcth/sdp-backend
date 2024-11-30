from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.conversation import Conversations
from database.content import Contents

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.get('/conversation')
@jwt_required()
def get_user_conversation():
    current_user = get_jwt_identity()
    conversation = Conversations()
    res = conversation.find_by_user_id(current_user["_id"])
    return jsonify(res), 200

@bp.get('/conversation/<id>')
@jwt_required()
def get_conversation_content(id):
    conversation = Conversations()
    conversation.find_by_id(id)
    data = []
    for text in conversation.contents:
        content = Contents()
        content.find_by_id(text)
        data.append(content.__dict__)
    return jsonify(data), 200

@bp.post('/content/<id>/rate')
@jwt_required()
def rate_content(id):
    content = Contents()
    content.find_by_id(id)
    data = request.json

    content.bad_response = True
    content.feedback = data['feedback']
    content.save_to_db()
    
    return jsonify({
        "message": "Thank you for your feedback"
    }), 200 