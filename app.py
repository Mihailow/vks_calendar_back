import datetime

from flask import Flask, request, send_from_directory, redirect
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)


def aaaaaaaa(name, request):
    with open(f"{name}.txt", "a+") as file:
        try:
            file.write('\njson: ' + str(request.json))
        except:
            pass
        try:
            file.write('\nfiles: ' + str(request.files))
        except:
            pass
        try:
            file.write('\nform: ' + str(request.form))
        except:
            pass
        try:
            file.write('\nargs: ' + str(request.args))
        except:
            pass
        try:
            file.write('\nrange: ' + str(request.range))
        except:
            pass
        try:
            file.write('\ndata: ' + str(request.data))
        except:
            pass
        try:
            file.write('\nvalues: ' + str(request.values))
        except:
            pass
        try:
            file.write('\nheaders: ' + str(request.headers))
        except:
            pass


@app.route('/api/test', methods=['POST'])
def test():
    aaaaaaaa("test", request)
    return "ok"


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
    # app.run(host="91.234.96.147", port=80)
