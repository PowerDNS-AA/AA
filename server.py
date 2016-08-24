import os

from flask import Flask, render_template, request
from flask import json
from flask import send_from_directory

from libs.classes import Resolve

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


@app.route("/monitor-index")
def monitor_index():
    data = []
    for dirname, dirnames, filenames in os.walk('monitors'):
        for filename in filenames:
            with open('monitors/' + filename) as data_file:
                temp = json.load(data_file)

                if os.path.exists('zones/' + temp['domain'] + ".json"):
                    with open('zones/' + temp['domain'] + ".json") as data_file:
                        zone = json.load(data_file)
                        for i in zone["A"]:
                            if i['address'] == temp['subDomain'] or i['address'] == temp['domain'] + ".":
                                domainARecord = i['content']
                                break
                print(domainARecord)
                if domainARecord and domainARecord not in temp['A']:
                    temp['A'].append(domainARecord)
                data.append(temp)

    return render_template("index.html", content="monitor-index.html", monitors=data)

@app.route("/api/v1/lookup/<domain>./<type>")
def lookup(domain, type):
    resolve = Resolve(domain=domain, type=type)
    return json.dumps({'result': resolve.lookup().response})


@app.route("/api/v1/getDomainMetadata/<domain>./<type>")
def get_domain_metadata(domain, type):
    return json.dumps({'result': 0})


if __name__ == "__main__":
    app.run(port=4998, host="0.0.0.0")
