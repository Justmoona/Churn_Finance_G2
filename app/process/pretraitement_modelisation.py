import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.metrics import accuracy_score, recall_score, precision_score, auc, roc_auc_score, roc_curve,f1_score
from sklearn.svm import SVC

file_path = 'app/data/churn.csv' 
 
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def object_to_int(dataframe_series):
    if dataframe_series.dtype=='object':
        dataframe_series = LabelEncoder().fit_transform(dataframe_series)
    return dataframe_series

# Definition de la methode du model
def RFC(train_x, test_x, y_train, y_test):
    model_rfc=RandomForestClassifier()
    model_rfc.fit(train_x, y_train)
    # Prediction
    y_test_pred_rfc = model_rfc.predict(test_x)
    # Calcul des metriques
    as_rfc = accuracy_score(y_test,y_test_pred_rfc)
    ps_rfc = precision_score(y_test,y_test_pred_rfc)
    rs_rfc = recall_score(y_test,y_test_pred_rfc)
    f1_rfc = f1_score(y_test,y_test_pred_rfc)
    print('Accuracy Score RFC:',round(as_rfc*100,2),"%")
    print('Precision Score RFC:',round(ps_rfc*100,2),"%")
    print('Recall Score RFC:',round(rs_rfc*100,2),"%")
    print('F1 Score RFC:',round(f1_rfc*100,2),"%")
    print("######### Matrix de confusion ##########")
    print(confusion_matrix(y_test, y_test_pred_rfc))
    # cm = confusion_matrix(y_test, y_test_pred_rfc)
    # sns.heatmap(cm,annot=True,fmt="d")
    print("######### DataFrame accuracy ##########")
    results = pd.DataFrame([['Random Forest Classifier',as_rfc,ps_rfc,rs_rfc,f1_rfc]],columns=['Model','Accuracy','Precision','Recall','F1'])
    print(results)


def steps():
    # Importation du dataset
    df = load_data(file_path)
    print(df.head())
    print(df.tail())

    # Exploration du dataset
    print(df.shape)
    print(df.info())

    # Analyse descriptive
    print(df.describe().T)

    # Manipulation des données
    df.drop(['RowNumber','CustomerId','Surname'],axis=1, inplace=True)
    df.rename(columns={"Exited":"Churned"},inplace=True)
    df["Churned"].replace({0:"No",1:"Yes"},inplace=True)

    # EDA (Analyse exploratoire des données)
    count = df["Churned"].value_counts()
    plt.figure(figsize=(12,4))
    plt.subplot(1,2,1)
    ax=sns.countplot(df["Churned"],palette="Set2")
    ax.bar_label(ax.containers[0],fontweight="black",size=15)
    plt.title("Distribution des clients désabonnés",fontweight="black",size=15,pad=20)
    plt.subplot(1,2,2)
    plt.pie(count.values, labels=count.index, autopct="%1.1f%%",colors=sns.set_palette("Set2"),
            textprops={"fontweight":"black"},explode=[0,0.1])
    plt.title("Distribution des clients désabonnés",fontweight="black",size=15,pad=20)
    plt.savefig('distributon.png', dpi=120)


    # Conversion des colonnes « objet » en « entier »
    df = df.apply(lambda x: object_to_int(x))
    df.rename(columns={"Churned":"Exited"},inplace=True)
    print(df.head())


    print("############################### Construction du model ###########################")
    ##### Séparation des données en train et test
    X = df.drop(columns = ['Exited'])
    Y = df.iloc[:,-1]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state = 42, stratify=Y)
    print('X_train {}'.format(X_train.shape))
    print('y_train {}'.format(X_test.shape))
    print('X_test  {}'.format(y_train.shape))
    print('y_test  {}'.format(y_test.shape))


    print("######### Proportion des deux classes ##########")
    print(pd.DataFrame(Y).value_counts(normalize=True))


    # Sur-échantillonnage
    X2 = X_train.copy()

    X2['Exited'] = y_train.values

    minority = X2[X2.Exited == 1]

    majority = X2[X2.Exited == 0]

    minority_upsampled = resample(minority, replace=True, n_samples=len(majority), random_state=1111)

    upsampled = pd.concat([majority, minority_upsampled])
    print(upsampled.head())

    print("######### Proportion des deux classes ##########")
    upsampled['Exited'].value_counts(normalize=True)


    ##### Séparation des données en train et test apres sur-echantillonnage
    X_train_up = upsampled.drop(columns = ['Exited'])
    y_train_up = upsampled.iloc[:,-1]

    X_train_up, X_test_up, y_train_up, y_test_up = train_test_split(X_train_up, y_train_up, test_size=0.3, random_state = 42, stratify=y_train_up)
    print('X_train_up {}'.format(X_train_up.shape))
    print('y_train_up {}'.format(X_test_up.shape))
    print('X_test_up  {}'.format(y_train_up.shape))
    print('y_test_up  {}'.format(y_test_up.shape))

    # Définition des données d'entrainement
    train_x = X_train_up
    train_y = y_train_up
    test_x = X_test_up
    test_y = y_test_up


    print("######### Normalisation ##########")
    # Normalisation
    scaler = MinMaxScaler()
    mod_scaler = scaler.fit(train_x)
    # mod_scale = scaler.fit(X_test)
    train_x = mod_scaler.transform(train_x)
    test_x = mod_scaler.transform(test_x)

    # Retransformation en DataFrame
    train_x = pd.DataFrame(train_x, columns = X.columns)
    test_x = pd.DataFrame(test_x, columns = X.columns)

    # Toute les variables sont entre 0 et 1
    train_x.head()
    test_x.head()
     
    print("######### Model Random Forest Classifier ##########")
    RFC(train_x,test_x,train_y,test_y)




if __name__ == '__main__':
    steps()