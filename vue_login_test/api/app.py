# app.py

##测试中
from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import model
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins='*')
socketio.init_app(app)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    username = ''
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
    result = model.check_credentials(username)
    response = {
        'status': result
    }
    return jsonify(response)


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    username = ''
    password = ''
    salt = ''
    pk = ''
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        pk = post_data.get('publicKey')
    result = model.register(username, password, pk)
    response = {
        'status': result
    }
    return jsonify(response)


@app.route('/api/get_friend', methods=['GET', 'POST'])
def get_friend():
    username = ''
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
    result = model.get_friend(username)
    # [{friend: 'user2'}]

    return jsonify(result)


# @app.route('/api/get_publicKey',methods=['GET', 'POST'])
# def get_publicKey():
#     username = ''
#     if request.method == 'POST':
#         post_data = request.get_json()
#         username = post_data.get('username')
#     result = model.get_publicKey(username)
#
#     return jsonify(result)

@app.route('/api/get_chat', methods=['GET', 'POST'])
def get_chat():
    username = ''
    friendname = ''
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
        friendname = post_data.get('friendname')
    result = model.get_chat(username, friendname)
    pk = model.get_publicKey(friendname)
    response = {
        'publicKey': pk,
        'history': result
    }
    return jsonify(response)


@app.route('/api/get_question', methods=['GET', 'POST'])
def get_question():
    result = model.get_question()
    print(result)
    return jsonify(result)


@app.route('/api/get_comment', methods=['GET', 'POST'])
def get_comment():
    post_data = request.get_json()
    qid = post_data.get('qid')
    result = model.get_comment(qid)
    return jsonify(result)


@app.route('/api/add_chat', methods=['GET', 'POST'])
def add_chat():
    username = ''
    friendname = ''
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
        friendname = post_data.get('friendname')
        message = post_data.get('message')
    result = model.add_chat(username, friendname, message)
    response = {
        'status': result
    }
    return jsonify(response)


@app.route('/api/add_question', methods=['POST'])
def add_question():
    post_data = request.get_json()
    title = post_data.get('title')
    description = post_data.get('description')
    provider = post_data.get('provider')
    private = post_data.get('private')
    result = model.add_question(title, description, provider, private)
    response = {
        'status': result
    }
    return jsonify(response)


@app.route('/api/add_friend', methods=['GET', 'POST'])
def add_friend():
    if request.method == 'POST':
        post_data = request.get_json()
        userName = post_data.get('userName')
        friendName = post_data.get('friendName')
    result = model.add_friend(userName, friendName)
    response = {
        'status': result
    }
    return jsonify(response)


@app.route('/api/add_comment', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        post_data = request.get_json()
        qid = post_data.get('qid')
        answer = post_data.get('answer')
        user = post_data.get('user')
    result = model.add_comment(qid, answer, user)
    response = {
        'status': result
    }
    return jsonify(response)


@app.route('/api/file', methods=['GET', 'POST'])
def store_File():
    f = request.files['file']
    try:
        # 构造图片保存路径
        print(f)
        file_path = 'File/' + f.filename
        f.save('./' + file_path)
        full_path = os.path.join(app.root_path, file_path)
        # 保存图片
        response = full_path
    except Exception:
        response = None
    return jsonify(response)


@app.route('/api/add_file', methods=['GET', 'POST'])
def add_file():
    if request.method == 'POST':
        post_data = request.get_json()
        filename = post_data.get('name')
        title = post_data.get('title')
        url = post_data.get('url',)
        username = post_data.get('user')
        f_format = post_data.get('format')
    result = model.add_file(filename, title, url, username, f_format)
    print(result)
    response = {
        'status': result
    }
    return jsonify(response)


@app.route('/api/get_user', methods=['GET', 'POST'])
def get_user():
    result = model.get_user()
    return jsonify(result)


@app.route('/api/get_file', methods=['GET', 'POST'])
def get_file():
    result = model.get_file()
    return jsonify(result)


@socketio.on('message')
def message(json):
    from_user = json.get('user')
    to_user = json.get('to')
    msg = json.get('msg')
    messageData = {
        "from_user": from_user,
        "to_user": to_user,
        "message": msg
    }
    print('RECEIVED: ' + str(messageData))
    socketio.emit('RESPONSE', messageData)
    return make_response(jsonify(messageData))


@socketio.on('test')
def test():
    print("TEST")


# @socketio.on('message')
# def handle_message(message):
#     print(message)
#     send(message,broadcast=True)
#
#
# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})

# run Flask app
if __name__ == "__main__":
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
    # app.run()
