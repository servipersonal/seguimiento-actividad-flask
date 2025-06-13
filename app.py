import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = None
    error = None

    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.csv'):
            try:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)

                df = pd.read_csv(filepath)

                # Validar columnas requeridas
                columnas_requeridas = {'Día', 'Pasos', 'Calorías', 'Minutos'}
                if not columnas_requeridas.issubset(df.columns):
                    error = "El archivo CSV debe contener las columnas: Día, Pasos, Calorías y Minutos."
                else:
                    dias = df['Día'].tolist()
                    pasos = df['Pasos'].tolist()
                    calorias = df['Calorías'].tolist()
                    minutos = df['Minutos'].tolist()

                    mensaje = "Archivo cargado correctamente ✅"
                    return render_template('index.html', labels=dias, pasos=pasos, calorias=calorias, minutos=minutos, mensaje=mensaje, error=None)
            except Exception as e:
                error = f"Error al procesar el archivo: {str(e)}"
        else:
            error = "Por favor selecciona un archivo .csv válido."

    return render_template('index.html', labels=[], pasos=[], calorias=[], minutos=[], mensaje=mensaje, error=error)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)