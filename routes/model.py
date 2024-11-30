from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.conversation import Conversations
from database.content import Contents
from models.tranformer import testModel, model_api
from models.top_k import get_top_k

bp_model = Blueprint('model', __name__, url_prefix='/api/model')
bp = Blueprint('model', __name__, url_prefix='/api')

@bp_model.post('/test')
def test_model():
    testModel()
    return {}, 200

@bp.post('/customer/question')
def generate_question_customer():
    data = request.json
    try:
        success, answer_part, explain_part = model_api(
            data["question"], data["answers"], data["version"])
        top_k = get_top_k(data["question"], 15)
        if success:
            return jsonify({
                "correct_answer": answer_part,
                "explanation": explain_part,
                "top_k": top_k
            })
        else:
            [grade, lesson] = top_k.split('_')
            return jsonify({
                "message": f"Waiting for loading model, but you can search the answer in history book grade {grade} lesson {lesson}"
            }), 400
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@bp.post('/user/question')
@jwt_required()
def generate_question_user():
    current_user = get_jwt_identity()
    data = request.json
    try:
        success, answer_part, explain_part = model_api(
            data["question"], data["answers"], data["version"])
        top_k = get_top_k(data["question"], 15)
        
        if success:
            conversation = Conversations(
                current_user["_id"], [], data["question"])

            if data["conversationId"]:
                conversation.find_by_id(data["conversationId"])
            else:
                conversation.save_to_db()

            contentId = conversation.contents
            ask = Contents(conversation._id, "ask",
                         data["question"], data["answers"])
            ask.save_to_db()
            contentId.append(ask._id)
            
            respone = Contents(conversation._id, "answer",
                             data["question"], data["answers"], 
                             explain_part, answer_part,
                             version=data["version"], top_k=top_k)
            respone.save_to_db()
            contentId.append(respone._id)
            
            conversation.contents = contentId
            conversation.save_to_db()

            return jsonify({
                "correct_answer": answer_part,
                "explanation": explain_part,
                "conversation_id": conversation._id,
                "answer_id": respone._id,
                "top_k": top_k
            })
        else:
            [grade, lesson] = top_k.split('_')
            return jsonify({
                "message": f"Waiting for loading model, but you can search the answer in history book grade {grade} lesson {lesson}"
            }), 400
    except ValueError as e:
        return jsonify({"message": str(e)}), 400 