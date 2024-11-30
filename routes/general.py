from flask import Blueprint, request, jsonify
from database.settings import Settings
from database.links import Links
from database.answers import Answers

bp = Blueprint('general', __name__, url_prefix='/api')


@bp.get('/answers')
def get_answers():
    params = request.args
    name = params.get('name')
    setting = Settings()
    result = setting.find_by_id(name)
    return jsonify({
        "message": "success"
    }), 200

@bp.delete('/delete')
def test_delete():
    link = Links()
    answers = Answers()
    link.delete_by_month()
    answers.delete_by_month()
    return jsonify({
        "message": "success"
    }), 200