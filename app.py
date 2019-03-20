import os
from flask import Flask, request, jsonify, Response, send_file
import Process
import Ipaddress
from werkzeug.utils import secure_filename
import ast

UPLOAD_FOLDER = 'media'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ip = Ipaddress.getIP()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'


def return_dict(folder):
    dict_here = []
    i = 1
    with open("music/{}.txt".format(folder)) as f:
        for line in f:
            line = line.rstrip('\n')
            line = line.split("|")
            dict_here.append({'id': i, 'link': line[0], 'image': line[1]})
            i += 1

    return dict_here


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print("\n\n\n")
    if request.method == 'POST':
        print("=" * 25)
        print(request.files['file'], "<---")
        print("=" * 25)
        file = request.files['file']
        folderName = request.form['name']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], folderName)):
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folderName))
            file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], folderName), filename))
            filename = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], folderName), filename)
            print(filename)
            emotions = Process.process(filename)
            return emotions, 201
    if request.method == 'GET':
        return jsonify({"Hello": "1"}), 200
    return


@app.route('/music/<string:stream_folder>/<int:stream_id>', methods=['GET', 'POST'])
def streammp3(stream_folder, stream_id):
    def generate(folder):
        data = return_dict(folder)
        for item in data:
            if int(item['id']) == int(stream_id):
                song = item['link']
                break
        with open(song, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)

    return Response(generate(stream_folder), mimetype="audio/mp3")


@app.route('/music/<string:stream_folder>/<int:stream_id>/<int:image>', methods=['GET', 'POST'])
def imager(stream_folder, stream_id, image):
    data = return_dict(stream_folder)
    for item in data:
        if int(item['id']) == int(stream_id):
            image = item['image']
            break

    return send_file(image, mimetype='image/jpg')


if __name__ == '__main__':
    app.debug = True
    app.run(host=ip, port=5000)
