from flask import Flask, request, render_template
from flask_socketio import SocketIO
import socket

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisaprettysecuresecretkeyifidosaysomyself'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('session.html')

@app.route('/qr',methods=["GET"])
def get_qr():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return render_template('qr.html',server_url="http://"+IPAddr+":5000")

def messageReceived(methods=['GET', 'POST']):
    pass

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    if "message" in json and len(json["message"])>0:
        add_message(json)
        socketio.emit('my response', get_messages(), callback=messageReceived)

global messages
messages = []

def get_messages():
    global messages
    return messages

def add_message(data):
    global messages
    messages += [{
        "name" : data["name"],
        "message" : data["message"]
    }]

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)