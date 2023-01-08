from flask import Flask, request, render_template, redirect, url_for, session
import json 
import os
import validators
import ipaddress
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oYbTYrb9ggsGKqsbB3PHe2xNNvaEdmPeh'
socketio = SocketIO(app,)
auth = HTTPBasicAuth()

#http basic auth

try:
    with open("users.json", "r") as file:
        users = json.load(file)
except FileNotFoundError:
    print("no users.json file detected please create a user via running 'docker exec containername python3 createuser.py' otherwise you will not be able to log in")
    users = {}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

def GetRouters():
    path = "./infrared/data/configs/"
    files = []

    for r, d, f in os.walk(path):
        for file in f:
            if ".json" in file:
                files.append(file.replace(".json", ""))
    return files

def ExtractJson():
    path = "./infrared/data/configs/"
    files = []

    for r, d, f in os.walk(path):
        for file in f:
            if ".json" in file:
                data = {}
                filepath = os.path.join(r, file)
                with open(filepath) as jsonfile:
                    data = json.load(jsonfile)
                temp = {}
                temp["domainName"] = data["domainName"]
                temp["proxyTo"] = data["proxyTo"]
                files.append(temp)
    return files


@app.route('/')
@auth.login_required
def index():
    return render_template("index.html", items=ExtractJson(), deleteselect=GetRouters())

@app.route('/deleteroute', methods=["POST"])
@auth.login_required
def deleteroute():
    try:
        deleteselect = request.form['deleteselect']
        os.remove("./infrared/data/configs/" + deleteselect + ".json")
        return redirect("/", code=302)
    except KeyError:
        return redirect("/", code=302)

@app.route('/newroute', methods=["POST"])
@auth.login_required
def newroute():
    domainname = request.form['domainname'].lower()
    IPAddr = request.form['IPAddr']
    Port = request.form['Port']

    if not validators.domain(domainname):
        return 'Invalid domain name: <a href="/">Go back?</a>'


    try:
       ip_object = ipaddress.ip_address(IPAddr)
    except ValueError:
        return 'Invalid IP address: <a href="/">Go back?</a>'

    if int(Port) < 0 or int(Port) > 65535:
        return 'Invalid Port: <a href="/">Go back?</a>'


    proxyTo = IPAddr + ":" + Port

    # create the json file as a dict
    jsonout = {}
    jsonout["domainName"] = domainname
    jsonout["proxyTo"] = proxyTo
    jsonout["listenTo"] = "0.0.0.0:25565"
    jsonout["disconnectMessage"] = "Goodbye"
    offlineStatus = {"motd": "Server is currently offline :("}
    jsonout['offlineStatus'] = offlineStatus

    # write config out to json file
    with open("./infrared/data/configs/" + domainname + ".json", 'w', encoding='utf-8') as file:
        json.dump(jsonout, file, ensure_ascii=False, indent=4)

    return redirect("/", code=302)


if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=False, use_reloader=False, host='0.0.0.0', port=5000)