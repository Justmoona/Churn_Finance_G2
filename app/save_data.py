from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pandas as pd
import pymysql

save_data = Flask(__name__)

# Configuration de la base de données MySQL
save_data.config['MYSQL_HOST'] = 'localhost'
save_data.config['MYSQL_USER'] = 'root'  # Utilisateur MySQL
save_data.config['MYSQL_PASSWORD'] = ''  # Mot de passe MySQL
save_data.config['MYSQL_DB'] = 'churn_finance'  # Base de données MySQL

# Mode débogage
save_data.config["DEBUG"] = True

# specification du fichier CSV
UPLOAD_FOLDER = 'app/data'
save_data.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE']

def get_db():
    return pymysql.connect(
        host=save_data.config['MYSQL_HOST'],
        user=save_data.config['MYSQL_USER'],
        password=save_data.config['MYSQL_PASSWORD'],
        db=save_data.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )


# URL par defaut
@save_data.route('/')
def index():
    return render_template('upload_data.html')


# Methode permettant d'uploader un fichier
@save_data.route("/", methods=['POST'])
def uploadFiles():
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(save_data.config['UPLOAD_FOLDER'], uploaded_file.filename)
           print(file_path)
           uploaded_file.save(file_path)
           parseCSV()
      return redirect(url_for('index'))


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

if (__name__ == "__main__"):
     save_data.run(port = 8000)

