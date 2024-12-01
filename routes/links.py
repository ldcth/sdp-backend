from flask import Blueprint, request, jsonify
from bson import ObjectId
from database.links import Links
from database.answers import Answers
from services.crawl import Test_Chitiet_HTML
import math
from flask_jwt_extended import jwt_required
bp = Blueprint('links', __name__, url_prefix='/api/links')

@bp.get('/')
@jwt_required()
def get_links():
    print(1)
    page = int(request.args.get('page', 0))
    per_page = int(request.args.get('per_page', 0))
    res = Links()
    result = res.get_all_links(page, per_page)
    return jsonify(result), 200

@bp.delete('/<id>')
def delete_link(id):
    link = Links()
    ans = Answers()
    try:
        link.find_by_id(id)
        for answer_id in link.questions:
            data = str(answer_id)
            ans.delete_by_id(data)
        link.delete_by_id(id)
        return jsonify({"message": "Delete success"}), 200
    except:
        return jsonify({"message": "Delete fail"}), 400

@bp.get('/<id>')
def get_link_detail(id):
    try:
        res = Links()
        result = res.find_by_id(id)
        if result:
            return jsonify(res.__dict__), 200
        return jsonify({"message": "Not found"}), 404
    except:
        return jsonify({}), 400

@bp.get('/<id>/answers')
def get_link_answers(id):
    link = Links()
    link.find_by_id(id)
    answers = Test_Chitiet_HTML(link.name)
    return jsonify(answers), 200

@bp.post('/<id>/crawl')
def crawl_answers_by_link(id):
    link = Links()
    link.find_by_id(id)
    answers = Test_Chitiet_HTML(link.name)
    questions = []
    for data in answers:
        if len(data) == 4:
            has_nan = False
            for key, value in data.items():
                if isinstance(value, float) and math.isnan(value):
                    has_nan = True
                    break
            if not has_nan:
                answer = Answers(data["question"], data["answers"],
                               data["explanation"], data["correct_answer"], ObjectId(id))
                answer.save_to_db()
                questions.append(ObjectId(answer._id))

    link.questions = questions
    link.save_to_db()
    return jsonify(answers), 200 