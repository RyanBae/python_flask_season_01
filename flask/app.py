from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from database import init_db
from database import db_session, Base, engine
from flask import redirect
from flask import flash
import base64
import os
from werkzeug.utils import secure_filename
from models.Members import Members
from flask_socketio import SocketIO
import cv2
from video import video

STATIC_FOLDER = 'assets'
app = Flask(__name__, static_folder=STATIC_FOLDER)
app.secret_key = 'some_secret'
socketio = SocketIO(app)

init_db()
# Base.metadata.create_all(bind=engine)

title = "Flask World!!"
image_path = './assets/image'


@app.route('/')
def index():
    # flash("환영합니다!!!")
    return render_template('index.html', title=title)


@app.route('/list')
def list():
    # 딕셔너리 자료형
    if len(request.args.to_dict()) == 0:
        return 'No parmeter'

    paramMap = {}
    for key in request.args.to_dict().keys():
        paramMap = {key: request.args[key]}

    # type = 0 : db
    # type = 1 : text file
    if paramMap['type'] == '0':
        print(">>> DB")
        data_type = 'DataBase'
        queries = db_session.query(Members)
        entries = [dict(id=q.id, name=q.name, age=q.age, create_datetime=q.create_datetime, delete_datetime=q.delete_datetime)
                   for q in queries]
        # db_session.flush()
        db_session.close()

    else:
        print(">>> TEXT")
        data_type = 'TextFile'
        f = open("members.txt", "r")
        contents = f.read().split('\n')
        entries = []
        for line in contents:
            print(line.split(','))
            l = line.split(',')
            if l[0] != '':
                entries.append({'id': l[0], 'name': l[1], 'age': l[2]})

        f.close()

    return render_template('list.html', title=title, dataType=data_type, members=entries)


@app.route('/view_form', methods=['GET', 'POST'])
def view_form():
    if request.method == 'GET':
        print("> Methods : GET")
        member = ''
        if len(request.args.to_dict()) != 0:
            paramMap = {}
            for key in request.args.to_dict().keys():
                paramMap = {key: request.args[key]}

            member = db_session.query(Members).filter(
                Members.id == paramMap['id']).first()

            # db_session.flush()
            db_session.close()

        return render_template('view.html', title=title, member=member)

    elif request.method == 'POST':
        print("> Methods : POST")

        # open("yourfile.ext", "rb") as image_file:
        # encoded_string = base64.b64encode(image_file.read())
        print(request.files['image_file'])

        image_file_path = file_upload(request)

        in_member = Members(
            request.form['name'], request.form['age'], None, None, image_file_path)
        db_session.add(in_member)

        # flush() 는 SQL 문을 데이터베이스로 보냅니다.
        # commit() 은 트랜잭션을 커밋합니다.

        # session : 데이터베이스와 연결된 세션, 즉 접속된상태며 db 처리를 위해선 session 필요.
        # 저장, 수정, 삭제 를 commit() 를 통해야 하며, 롤백은 rollback() 함수 사용.
        db_session.commit()
        # 커밋 되고 연결된 객체가 닫힘.
        db_session.flush()
        row_insert_to_add_text(in_member)

        # return redirect('/view_form?id='+str(in_member.id))
        return redirect('/list?type=0')


@app.route('/getImage', methods=['POST'])
def get_member_image_file():
    member = db_session.query(Members).filter(
        Members.id == request.form['id']).first()

    # db_session.flush()
    db_session.close()
    res = False
    if member.image_file == '':
        print("==>?")
        res = True

    result = {'imageName': member.image_file}
    return result


@app.route('/video')
def video_page():
    print("Video")
    return render_template('stream.html', title=title, type='1')


def gen(video):
    while True:
        # get camera frame
        frame = video.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream')
def video_stream():
    print("Video Streaming")
    return render_template('stream.html', title=title, type='0')


@socketio.event
def connect():
    print('==> Flask SocketIO Connect ! ')
    socketio.emit('received', 'flask Connect !')


@socketio.event
def disconnect():
    print(" Socket IO disConnect !!!")
    socketio.emit('disconnected', 'disconnect')


@socketio.on('streaming')
def handle_event(json, methods=['GET', 'POST']):
    # print("Received :: "+json['img'])
    # cv2.imshow('streaming_img', json['img'])
    # print("Received :: "+json)
    # socketio.emit('received', 'test')
    socketio.emit('view', json['img'])


def file_upload(req):
    file = req.files['image_file']
    if file.filename != '':
        filename = secure_filename(file.filename)
        # os.makedirs('../assets/image', exists_ok=True)
        file.save(os.path.join(image_path, filename))
    else:
        filename = None

    return filename


def row_insert_to_add_text(member):
    print("======== > Row Insert To Add Text")
    flag = os.path.isfile('members.txt')
    if flag == True:
        f = open("members.txt", "a")
    else:
        f = open("members.txt", "w")

    f.write(str(member.id)+','+member.name+','+member.age+',' +
            str(member.create_datetime)+','+str(member.delete_datetime)+','+str(member.image_file)+'\n')
    f.close()


if __name__ == '__main__':
    # socketio.run(app)
    # app.run(debug=True, host='127.0.0.1', port='5000')
    app.run(debug=True, host='0.0.0.0', port='5000')
