import pickle
import json
from flask import Flask,request,app,jsonify,url_for,render_template,redirect
import numpy as np
import pandas as pd
import pymysql
import os
from os.path import join, dirname, realpath


app=Flask(__name__)

# Charger le modele
rfcmodel=pickle.load(open('app/model/rfcmodel.pkl','rb'))
scalar=pickle.load(open('app/model/scaling.pkl','rb'))


# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Utilisateur MySQL
app.config['MYSQL_PASSWORD'] = ''  # Mot de passe MySQL
app.config['MYSQL_DB'] = 'churn_finance'  # Base de données MySQL

# Mode débogage
app.config["DEBUG"] = True

# specification du fichier CSV
UPLOAD_FOLDER = 'app/data'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE']

def get_db():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )


class Data():
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

# Methode permettant de stocker le contenu du fichier CSV dans la base de donnee MySQL
def parseCSV():
      # Le nom des colonnes du fichier CSV
      col_names = ['RowNumber', 'CustomerId', 'Surname', 'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Exited']
      # Utilisez Pandas pour analyser le fichier CSV
      csvData = pd.read_csv('app/data/churn.csv')
      # Nous allons parcourez chauqes du fichier CSV
      for i,row in csvData.iterrows():
             sql = "INSERT INTO churn (RowNumber, CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
             value = (row['RowNumber'], row['CustomerId'], row['Surname'], row['CreditScore'], row['Geography'], row['Gender'], row['Age'], row['Tenure'], row['Balance'], row['NumOfProducts'], row['HasCrCard'], row['IsActiveMember'], row['EstimatedSalary'], row['Exited'])
            #  print(value)
             cur = get_db().cursor()
             # cur.execute(sql, value, if_exists='append')
             cur.execute(sql, value)
             cur.connection.commit()
             cur.close()
             value = (row['RowNumber'], row['CustomerId'], row['Surname'], row['CreditScore'], row['Geography'], row['Gender'], row['Age'], row['Tenure'], row['Balance'], row['NumOfProducts'], row['HasCrCard'], row['IsActiveMember'], row['EstimatedSalary'], row['Exited'])



# URL par defaut
@app.route('/')
def index():
    return render_template('index.html')


# URL pour uploader un fichier
# @app.route('/')
# def upload():
#     return render_template('upload_data.html')


# Methode permettant d'uploader un fichier
@app.route("/", methods=['POST'])
def uploadFiles():
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
           print(file_path)
           uploaded_file.save(file_path)
           parseCSV()
      return redirect(url_for('index'))
    #   return render_template('index.html')


# URL pour la prediction
@app.route('/predict_api',methods=['POST'])
# def predict_api(data: Data):
def predict_api():
    data=request.json['data']
    # data = data.dict()
    print('Donnees envoyer: => {}'.format(data))
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
    print('Variables d\'entrees: => {}'.format(new_data))
    output=rfcmodel.predict(new_data)
    print('Output du model => {}'.format(output[0]))
    # return jsonify(output[0])
    return json.dumps(output[0], default=int)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


