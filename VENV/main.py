from flask import Flask
from flask import render_template, request, redirect, url_for
import os
from werkzeug import secure_filename
import glob
import shutil


app = Flask(__name__)
#carpeta donde se subiran los archivos
app.config['UPLOAD_FOLDER'] = './archivos csv'


@app.route('/')
def upload_file():
    return render_template('Archivo.html')

@app.route('/upload', methods=['POST'])
def uploader():
    if request.method == 'POST':
        folder='archivos csv'
        #Eliminar archivo cada vez que ingrese otro
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder,the_file)
            
            
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)            
        f=request.files['archivo']
        filename=secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return "<h1>Archivo Subido exitosamente</h1>"
        

if __name__ == '__main__':
    app.run()