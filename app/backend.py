import pickle
import json
from flask import Flask,request,app,jsonify,url_for,render_template,redirect
import pymysql
import numpy as np
import pandas as pd
import os
# import psycopg2
# from os.path import join, dirname, realpath
# from pydantic import BaseModel

app=Flask(__name__)

# Charger le modele
rfcmodel=pickle.load(open('model/rfcmodel.pkl','rb'))
scalar=pickle.load(open('model/scaling.pkl','rb'))


# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'user'  # Utilisateur MySQL
app.config['MYSQL_PASSWORD'] = 'password'  # Mot de passe MySQL
app.config['MYSQL_DATABASE'] = 'churn_finance'  # Base de données MySQL

def get_db():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DATABASE'],
        cursorclass=pymysql.cursors.DictCursor
    )

def create_table_prediction():
    cur = get_db().cursor()
    # Créer uen base de données "data_HR"
    cur.execute("CREATE DATABASE IF NOT EXISTS churn_finance")
        # Création de la table "products" dans la base de données
    cur.execute('''CREATE TABLE IF NOT EXISTS churn_finance.predictions (
            CreditScore FLOAT,
            Geography INT,
            Gender BOOLEAN,
            Age FLOAT,
            Tenure FLOAT,
            Balance FLOAT,
            NumOfProducts INT,
            HasCrCard BOOLEAN,
            IsActiveMember BOOLEAN,
            EstimatedSalary FLOAT,
            Exited BOOLEAN
        )''')


def create_table():
    # Création d'un curseur
    cur = get_db().cursor()
    # Créer uen base de données "data_HR"
    cur.execute("CREATE DATABASE IF NOT EXISTS churn_finance")
    # Création de la table "products" dans la base de données
    cur.execute('''CREATE TABLE IF NOT EXISTS churn_finance.churn (
        RowNumber INT AUTO_INCREMENT PRIMARY KEY,
        CustomerId VARCHAR(255),
        Surname VARCHAR(255),
        CreditScore INT,
        Geography VARCHAR(255),
        Gender VARCHAR(255),
        Age INT,
        Tenure INT,
        Balance FLOAT,
        NumOfProducts INT,
        HasCrCard INT,
        IsActiveMember INT,
        EstimatedSalary FLOAT,
        Exited INT
    )''')


# Mode débogage
app.config["DEBUG"] = True

# specification du fichier CSV
UPLOAD_FOLDER = 'app/data'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE']

# Methode permettant de stocker le contenu du fichier CSV dans la base de donnee MySQL
def parseCSV():
      # Le nom des colonnes du fichier CSV
      col_names = ['RowNumber', 'CustomerId', 'Surname', 'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Exited']
      # Utilisez Pandas pour analyser le fichier CSV
      csvData = pd.read_csv('app/data/churn.csv')
      # Nous allons parcourez chauqes du fichier CSV
      for i,row in csvData.iterrows():
             create_table()
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


@app.route('/predict',methods=['POST'])
def predict():
    # Recuperation du json provenant du front
    data=request.json['inputs']
    print('Donnees envoyer: => {}'.format(data))
    print(np.array(list(data.values())).reshape(1,-1))
    # transformer le data redimentionner
    new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
    # Stoper les inputs dans un dataframe
    input_df = pd.DataFrame(new_data, index=[0])
    print(input_df)
    print('Variables d\'entrees: => {}'.format(new_data))
    # Prediction des valeurs
    output=rfcmodel.predict_proba(new_data)[0][1]
    print('Output du model => {}'.format(output))
    # Appel de la methode pour creer la table
    create_table_prediction()
    # Insertion des inputs dans la table predictions 
    sql = "INSERT INTO predictions (CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    value = (
        float(input_df.iloc[0, 0]),
        float(input_df.iloc[0, 1]),
        float(input_df.iloc[0, 2]),
        float(input_df.iloc[0, 3]),
        float(input_df.iloc[0, 4]),
        float(input_df.iloc[0, 5]),
        float(input_df.iloc[0, 6]),
        float(input_df.iloc[0, 7]),
        float(input_df.iloc[0, 8]),
        float(input_df.iloc[0, 9]),
        float(output)
    )
    print(value)
    cur = get_db().cursor()
    cur.execute(sql, value)
    cur.connection.commit()
    cur.close()
    return jsonify(output)


@app.route('/reporting')
def reporting():
    # Récupération d'une connexion à la base de données && Création d'un curseur pour exécuter des requêtes SQL
    cur = get_db().cursor()
    cur.execute("SELECT * FROM predictions")
    cur.connection.commit()
    predictions = cur.fetchall()
    cur.close()
    return jsonify(predictions)




if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


