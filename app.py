from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
import logging

from meteion import fire_post_event
import meteion
import onebot

import model

###Config
local_port   = 15000
meteion.config['PORT'] = 12019
onebot.config['PORT']  = 5700
###

### Flask{
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meteion.db'
app.config['SECRET_KEY'] = 'secret!'

db = SQLAlchemy(app)
socketio = SocketIO(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
### }Flask

### WEBHOOK Listener{
@app.route("/")
def hello_world():
    return "<p>Hello, FFXIV!</p>"

@app.route("/meteion/chat",methods=['GET','POST'])
def meteion_chat_listener():
    fire_post_event(request,"chat")
    return "OK"

@app.route("/meteion/event",methods=['GET','POST'])
def meteion_event_listener():
    fire_post_event(request,"event")
    return "OK"

@app.route("/meteion/partyfinder",methods=['GET','POST'])
def meteion_partyfinder_listener():
    fire_post_event(request,"partyfinder")
    return "OK"

@app.route("/meteion",methods=['GET','POST'])
def meteion_listener():
    fire_post_event(request,"heartbeat")
    return "OK"

@app.route("/report/rploc",methods=['GET','POST'])
def meteion_report_rploc():
    rp_logs=model.roleplay.RolePlayFinder.query.order_by(model.roleplay.RolePlayFinder.update_time.desc()).all()
    return render_template('rploc.html',rp_logs=rp_logs)
### }WEBHOOK Listener

if __name__ == '__main__':
    db.session.commit()
    meteion.load_all_plugins()
    socketio.run(app, port=local_port, host='0.0.0.0', debug=True)