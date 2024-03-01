import pickle
import json

from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app=Flask(__name__)

# Charger le modele
rfcmodel=pickle.load(open('model/rfcmodel.pkl','rb'))
scalar=pickle.load(open('model/scaling.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.json['data']
    print('Donnees renvoyer: => {}'.format(data))
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
    print('Variables d\'entrees: => {}'.format(new_data))
    output=rfcmodel.predict(new_data)
    print('Output du model => {}'.format(output[0]))
    # return jsonify(output[0])
    return json.dumps(output[0], default=int)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


