import os
from flask import Flask, flash, request, redirect, send_from_directory
from flask.helpers import make_response
from flask.templating import render_template
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/marce/Documents/uploads'
ALLOWED_EXTENSIONS = {'txt', 'GIF', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', 'exe', 'iso', 'mp4', 'hevc', 'mp3', 'wav', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)


# PÁGINA PRINCIPAL
class AppointmentController(Resource):
    def get(self):
        return make_response(render_template('index.html'))

    def post(self):
        if request.method == 'POST':

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
 
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return make_response(render_template('upload.html'))

# PÁGINA COM A LISTA DOS ARQUIVOS UPADOS
class UplodadedFiles(Resource):
    def get(self):
        pathFolder = 'C:/Users/marce/Documents/uploads/'
        array = os.listdir(pathFolder)
        
        extArray = []
        fileSizeArray = []
        
        for item in array:
            ext = item.split('.')
            extArray.append(ext[-1].upper())
            sizeFile = os.path.getsize(pathFolder + item)
            sizeFile /= 1000000
            sizeFile = f'{sizeFile:.2f}MB'
            fileSizeArray.append(sizeFile)
    
        arraySize = len(array)
        return make_response(render_template('list.html', array=array, extArray=extArray, fileSizeArray=fileSizeArray, arraySize=arraySize))


# DOWNLOAD DE ARQUIVO
class DownloadFiles(Resource):
    def get(self, name):
        return send_from_directory(app.config['UPLOAD_FOLDER'], name)


api.add_resource(AppointmentController, '/')
api.add_resource(UplodadedFiles, '/list')
api.add_resource(DownloadFiles, '/list/<name>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)