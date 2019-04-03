import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import threading
import json

from flask import Flask, render_template, jsonify, request, Response
from statsmodels.tsa.vector_ar.var_model import VAR

app = Flask(__name__)

y = None

@app.route('/ml')
def ml():
    print("enviando respuesta")

    if t.isAlive():
        return '500c'
    else:
        list_s = json.dumps(y.tolist())
        return Response(list_s,  mimetype="application/json")



def worker():
    data = pd.read_csv('Datos.csv', sep=",")
    data.index = data['Fecha ']
    data = data.drop(['Fecha '], axis = 1)
    print(data)
    values = data.values
    values = values.astype('float32')
    train = values[:,:]
    model = VAR(endog=train[:])
    model_fit = model.fit(maxlags=200, ic='aic')
    pred = model_fit.forecast(model_fit.y, steps = 30)
    print("--------------------------PREDICCION-----------------------------")
    print(pred[:,0])
    global y
    y = pred[:,0]
    #res= pd.Series(y).to_json(orient='values') 
    
    
t = threading.Thread(target=worker)
if __name__ == '__main__':
    t.start()
    app.run(debug=True) 
    