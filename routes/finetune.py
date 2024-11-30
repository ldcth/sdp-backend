from flask import Blueprint, request, jsonify
from database.finetune import Finetune
from models.finetuned import finetune_model
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

bp = Blueprint('finetune', __name__, url_prefix='/api/finetune')


@bp.post('/')
@jwt_required()
def finetune():
    url = finetune_model()
    finetuned = Finetune(100, url)
    finetuned.save_to_db()
    return jsonify(finetuned.__dict__), 200

@bp.get('/')
@jwt_required()
def get_finetune():
    finetuned = Finetune()
    data = finetuned.get_all()
    return jsonify(data), 200