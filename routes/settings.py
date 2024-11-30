from flask import Blueprint, request, jsonify
from database.settings import Settings

bp = Blueprint('settings', __name__, url_prefix='/api/settings')

@bp.get('/')
def get_setting():
    setting = Settings()
    res = setting.find_one()
    return jsonify(res), 200

@bp.post('/')
def create_setting():
    return jsonify({"message": "Setting created successfully"}), 200

@bp.put('/')
def update_setting():
    setting = Settings()
    res = setting.find_one()
    data = request.json
    setting.crawl = data["crawl"]
    setting.time = data["time"]
    setting.type = data["type"]
    setting.date = data["date"]
    setting.save_to_db()
    return jsonify({"message": "Setting update successfully"}), 200 