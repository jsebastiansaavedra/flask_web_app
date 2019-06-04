from flask import Flask
from flask import render_template, request, redirect, url_for
import os
from werkzeug import secure_filename
import glob
import shutil
from sklearn.externals import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
#carpeta donde se subiran los archivos
app.config['UPLOAD_FOLDER'] = '/'


@app.route('/')
def upload_file():
    return render_template('Archivo.html')

@app.route('/upload', methods=['POST'])
def uploader():
    if request.method == 'POST':
        folder='/'
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
        
        lr = joblib.load("modelo.pkl")
        valores = pd.read_csv("prueba.csv")
        valores['normAmount'] = StandardScaler().fit_transform(valores['Amount'].values.reshape(-1, 1))
        valores = valores.drop(['Time','Amount'],axis=1)
        X = valores.ix[:, valores.columns != 'Class']
        respuestas = lr.predict(X.values)
        tamaño = len(respuestas)
        return render_template("Respuesta.html", respuestas=respuestas, tamaño=tamaño)
        

if __name__ == "__main__":
    app.run()