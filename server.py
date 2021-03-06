import os
from flask import Flask, render_template, request
from flask import json
from flask import send_from_directory
from jinja2 import Template

app = Flask(__name__)


@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('templates/assets', path)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/")
def index():
    return render_template("index.html", content="dashboard.html")


@app.route("/zone-index")
def zone_index():
    data = []
    for dirname, dirnames, filenames in os.walk('zones'):
        for filename in filenames:
            with open('zones/' + filename) as data_file:
                data.append(json.load(data_file))

    return render_template("index.html", content="zone-index.html", zones=data)


@app.route("/zone-add")
def zone_add():
    data = None
    if request.args.get('domain'):
        with open('zones/' + request.args.get('domain') + '.json') as data_file:
            data = json.load(data_file)

    return render_template("index.html", content="zone-add.html", data=data)


@app.route("/zone-save", methods=["POST"])
def zone_save():
    if request.is_json:
        data = request.json
        with open('zones/' + data['domain'] + ".json", 'w') as outfile:
            json.dump(data, outfile)
        return "0"
    return "1"


@app.route("/zone-delete", methods=["POST"])
def zone_delete():
    if request.is_json:
        data = request.json
        os.remove('zones/' + data['domain'] + ".json")
        return "0"
    return "1"


if __name__ == "__main__":
    app.run(port=4998, host="0.0.0.0")
