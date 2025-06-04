import datetime

from flask import Flask, request, send_from_directory, redirect
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

@app.route('/api/get_info', methods=['POST'])
def get_info():
    data = request.form.to_dict()
    info = db.get_month_info(int(data["month"]), int(data["year"]))
    return info


@app.route('/api/insert_date_info', methods=['POST'])
def insert_date_info():
    data = request.form.to_dict()
    db.insert_date_info(data["date"], data["info"])
    date = datetime.datetime.strptime(data["date"], '%d.%m.%Y')
    info = db.get_month_info(date.month, date.year)
    return info


if __name__ == '__main__':
    app.run(port=80)
