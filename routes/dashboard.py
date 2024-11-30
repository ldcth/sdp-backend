from flask import Blueprint, jsonify
from datetime import datetime
from database.links import Links
from database.answers import Answers
from database.user import Users
from database.content import Contents

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.get('/')
def get_infor_dashboard():
    link = Links()
    answer = Answers()
    user = Users()
    content = Contents()

    total_content = content.get_total()
    total_content_feedback = content.get_total_feedback()
    type_feedback = content.get_type_feedback()

    total_users = user.get_total()

    links_data = link.get_lated_data()
    total_links = link.get_total()

    total_answers = answer.get_total()
    total_pending = link.get_pending()

    links_months = link.get_data_months()
    links_grown = 0
    if datetime.utcnow().month > 1:
        cur_month = links_months[datetime.utcnow().month - 1]
        last_month = links_months[datetime.utcnow().month - 2]
        links_grown = (cur_month - last_month) / last_month

    answers_months = answer.get_data_months()
    answers_grown = 0
    if datetime.utcnow().month > 1:
        cur_month = answers_months[datetime.utcnow().month - 1]
        last_month = answers_months[datetime.utcnow().month - 2]
        answers_grown = (cur_month - last_month) / last_month

    return jsonify({
        "contents": {
            "feedback": total_content_feedback,
            "no_feedback": total_content - total_content_feedback,
            "type_feedback": type_feedback
        },
        "users": {
            "total": total_users,
            "growth": True,
            "value": "0.0%"
        },
        "links": {
            "total": total_links,
            "growth": links_grown > 0,
            "value": str(abs(round(links_grown * 100, 2))) + "%",
            "per_months": links_months,
            "data": links_data
        },
        "answers": {
            "total": total_answers,
            "growth": answers_grown > 0,
            "value": str(abs(round(answers_grown * 100, 2))) + "%",
            "per_months": answers_months
        },
        "pending": {
            "total": total_pending,
        },
    }), 200 