from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import schedule
import threading
import time
from routes import init_app
# from services.crawl import crawl_data
from datetime import datetime
from database.settings import Settings
from database.links import Links
from database.answers import Answers
from database.record import Records
from bson import ObjectId
import math
from services.crawl import Tracnghiem_Lichsu_url, Chitiet_HTML, handle, Test_Chitiet_HTML

app = Flask(__name__)
app.config['SECRET_KEY'] = 'history-quiz'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

def crawl_data():
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
        # results.append(link.__dict__)
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

def my_job():
    setting = Settings()
    setting.find_one()
    current_date = datetime.now()
    time_str = current_date.strftime("%H:%M")
    print(current_date.day, current_date.weekday(), time_str)
    if setting.crawl:
        if setting.type == "month":
            if current_date.day == setting.date and time_str == setting.time:
                print("crawl")
                crawl_data()
        else:
            current_date = datetime.now()
            if current_date.weekday() == setting.date and time_str == setting.time:
                print("crawl")
                crawl_data()

def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Register all blueprints
init_app(app)

if __name__ == "__main__":
    # schedule.every(1).minutes.do(my_job)
    # schedule_t = threading.Thread(target=schedule_thread)
    # schedule_t.start()
    app.run(debug=True, port=3001, host='0.0.0.0')
