from flask import Blueprint, jsonify
from bson import ObjectId
from database.links import Links
from database.answers import Answers
from database.record import Records
from services.crawl import Tracnghiem_Lichsu_url, Test_Chitiet_HTML
import math
bp = Blueprint('crawl', __name__, url_prefix='/api/crawl')

@bp.post('/')
def crawl():
    urls_10 = Tracnghiem_Lichsu_url(
        "https://vietjack.com/bai-tap-trac-nghiem-lich-su-10/index.jsp")
    urls_11 = Tracnghiem_Lichsu_url(
        "https://vietjack.com/bai-tap-trac-nghiem-lich-su-11/index.jsp")
    urls_12 = Tracnghiem_Lichsu_url(
        "https://vietjack.com/bai-tap-trac-nghiem-lich-su-12/index.jsp")
    urls = urls_10 + urls_11 + urls_12
    
    current_urls = Links().get_all_links()
    new_links_to_add = []
    for link in urls:
        if link not in [existing_link['name'] for existing_link in current_urls] and len(new_links_to_add) < 1000:
            new_links_to_add.append(link)

    total_questions = 0
    for url in new_links_to_add:
        link = Links(url)
        link.save_to_db()
        answers = Test_Chitiet_HTML(url)
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
                                   data["explanation"], data["correct_answer"], ObjectId(link._id))
                    answer.save_to_db()
                    questions.append(ObjectId(answer._id))
        link.questions = questions
        link.save_to_db()
        total_questions += len(link.questions)

    record = Records(total_questions, new_links_to_add)
    record.save_to_db()
    return jsonify(record.__dict__), 200

@bp.get('/')
def get_crawl_history():
    record = Records()
    data = record.get_all()
    return jsonify(data), 200 