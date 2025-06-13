import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            df = pd.read_csv(filepath)
            dias = df['Día'].tolist()
            pasos = df['Pasos'].tolist()
            calorias = df['Calorías'].tolist()
            minutos = df['Minutos'].tolist()

            return render_template('index.html', labels=dias, pasos=pasos, calorias=calorias, minutos=minutos)

    return render_template('index.html', labels=[], pasos=[], calorias=[], minutos=[])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)