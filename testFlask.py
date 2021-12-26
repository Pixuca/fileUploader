import os
from flask import Flask, flash, request, redirect
from flask.helpers import make_response
from flask.templating import render_template
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/marce/Documents/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', 'exe', 'iso', 'mp4', 'hevc', 'mp3', 'wav', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)


# PÁGINA PRINCIPAL
class AppointmentController(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
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
                return f'O arquivo {file.filename} foi upado com sucesso!'

# PÁGINA COM A LISTA DOS ARQUIVOS UPADOS
class UplodadedFiles(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        path = 'C:/Users/marce/Documents/uploads'
        lista = os.listdir(path)
        return make_response(render_template('list.html', lista=lista))

api.add_resource(AppointmentController, '/')
api.add_resource(UplodadedFiles, '/list')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)