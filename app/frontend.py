import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
# import numpy as np
import pickle
import requests
import json
from streamlit_option_menu import option_menu
import os
import numpy as np
import pandas as pd


# Charger le modele
rfcmodel=pickle.load(open('model/rfcmodel.pkl','rb'))
scalar=pickle.load(open('model/scaling.pkl','rb'))
file_path = 'app/data/churn.csv'  # Replace with the path to your dataset

st.set_page_config(
    page_title="Churn finance",
    page_icon="👋",
)

# Load the dataset
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to preprocess user input
def preprocess_data(input_data):
    print('Donnees envoyer: => {}'.format(input_data))
    print(np.array(list(input_data.values())).reshape(1,-1))
    new_data=scalar.transform(np.array(list(input_data.values())).reshape(1,-1))
    print('Variables d\'entrees: => {}'.format(new_data))
    # output=rfcmodel.predict(new_data)
    st.subheader("Résultat")
    st.write("*Prediction:*")
    # output=rfcmodel.predict_proba(new_data)[0, 1]
    output=rfcmodel.predict_proba(new_data)[0][1]
    print('Output du model => {}'.format(output))
    return output


# Bout de code permettant de desactiver l'avertisement sur les   
st.set_option('deprecation.showPyplotGlobalUse', False)

def plot_churn_distribution(data):
    churn_counts = data['Exited'].value_counts()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=churn_counts.index, y=churn_counts.values)
    plt.title('Churn Distribution')
    plt.xlabel('Churn')
    plt.ylabel('Count')
    st.pyplot()

# Function to plot age distribution by churn
def plot_age_distribution(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='Age', hue='Exited', kde=True, bins=30, alpha=0.7)
    plt.title('Age Distribution by Churn')
    plt.xlabel('Age')
    plt.ylabel('Count')
    st.pyplot()

# Function to plot balance distribution by churn
def plot_balance_distribution(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='Balance', hue='Exited', kde=True, bins=30, alpha=0.7)
    plt.title('Balance Distribution by Churn')
    plt.xlabel('Balance')
    plt.ylabel('Count')
    st.pyplot()

# Function to plot categorical variable distribution by churn
def plot_categorical_distribution(data, column):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=data, x=column, hue='Exited')
    plt.title(f'{column} Distribution by Churn')
    plt.xlabel(column)
    plt.ylabel('Count')
    st.pyplot()



# Streamlit interface
def main():
    # horizontal menu
    selected = option_menu(None, ["Home", "Upload csv", "Reporting", 'Settings'], 
        icons=['house', 'cloud-upload', "list-task", 'gear'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
    selected

    st.sidebar.image('Images/Stop-Customer-Churn.png')
    st.sidebar.header('⏱ Taux de désabonnement des clients ??')
    st.sidebar.info(
            """
        Le présent modèle d’apprentissage automatique est capable de prédire si les clients d’une banque quittent ou non la banque.
            """
        )
    st.sidebar.caption('Projet data science Master2 churn finance groupe2.')

    # # vertical menu
    # with st.sidebar:
    #     selected = option_menu("Menu", ["Home", "Upload csv", "Reporting", 'Settings'], 
    #         icons=['house', 'cloud-upload', "list-task", 'gear'], 
    #         menu_icon="cast", default_index=0)
    #     selected

    if selected == "Home":
        # Load the dataset
        data = load_data(file_path)

        st.title('📈 Churn Prediction')
        # st.subheader("⏱ Loan Prediction")
        st.image('Images/Customer-Churn.png', use_column_width='auto')

        # Affichage de la dataFrame
        if st.checkbox("Afficher la dataframe"):
            st.dataframe(data.head())

        # code pour specifier l'emplacement du fichier CSS
        with open("app/statics/style.css") as f:
            st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

        # User input for features
        # L'ordre des champs est tres important pour l'obtention de resultats fiables
        credit_score = st.slider('Credit Score', min_value=300, max_value=850, step=1, value=500)
        geography = st.selectbox('Geography', ('France', 'Germany', 'Spain'),help="Selectionner une region")
        gender = st.selectbox('Gender', ('Femme', 'Homme'))
        age = st.slider('Age', min_value=18, max_value=100, step=1, value=30)
        tenure = st.slider('Tenure (in years)', min_value=0, max_value=10, step=1, value=5)
        balance = st.number_input('Balance', min_value=0.0, step=1.0, value=0.0)
        num_of_products = st.slider('Number of Products', min_value=1, max_value=4, step=1, value=1)
        has_cr_card = st.radio('Has Credit Card?', ('Yes', 'No'))
        is_active_member = st.radio('Is Active Member?', ('Yes', 'No'))
        estimated_salary = st.number_input('Estimated Salary', min_value=10000.00, max_value=200000.00, step=10000.00, value=50000.00)

        # Map radio button responses to binary values
        is_active_member = 1 if is_active_member == 'Yes' else 0
        has_cr_card = 1 if has_cr_card == 'Yes' else 0
        if geography == 'France':
            geography = 0
        elif geography == 'Germany':
            geography = 1
        else:
            geography = 2
        
        gender = 1 if gender == 'Homme' else 0


        input_data = {'CreditScore': credit_score,
                    'Geography': geography,
                    'Gender': gender,
                    'Age': age,
                    'Tenure': tenure,
                    'Balance': balance,
                    'NumOfProducts': num_of_products,
                    'HasCrCard': has_cr_card,
                    'IsActiveMember': is_active_member,
                    'EstimatedSalary': estimated_salary
                    }

        # When the user clicks the predict button
        if st.button('Predict'):
            # preprocess_data(input_data)
            # response = requests.post("http://127.0.0.1:5000/predict_api", json=input_data)
            # print(response)
            # prediction =response.text

            # Appel de la methode de prediction
            prediction = preprocess_data(input_data)
            churn = prediction >= 0.5
            output_prob = float(prediction)
            output = bool(churn)
            if output == False:
                st.write("<span class='diagnosis benign'>Ce client devrait rester</span>", unsafe_allow_html=True)
                # st.write(f"Probabilité churn (en pourcentage): {output_prob} %")
                st.write("**Probabilité churn (en pourcentage)**",round(output_prob*100,2),"%")
                # st.success('Le client devrait rester, avec une probabilité de {0} %'.format(output_prob))
            else:
                # st.write("<span class='diagnosis malicious'>On s’attend à ce que le client se désabonne</span>", unsafe_allow_html=True)
                st.warning('On s’attend à ce que le client se désabonne')
                st.write("**Probabilité (en pourcentage)**",round(output_prob*100,2),"%")




    if selected == "Upload csv":
        st.write("page upload file...")

    if selected == "Reporting":
        data = load_data(file_path)
        # Data visualization
        st.header('Data Visualization')
        # Select visualization type
        visualization_type = st.selectbox('Select Visualization:', ['Churn Distribution', 'Age Distribution by Churn',
                                                                    'Balance Distribution by Churn', 'Geography Distribution',
                                                                    'Gender Distribution', 'NumOfProducts Distribution',
                                                                    'HasCrCard Distribution'])
        # Plot selected visualization
        if visualization_type == 'Churn Distribution':
            plot_churn_distribution(data)
        elif visualization_type == 'Age Distribution by Churn':
            plot_age_distribution(data)
        elif visualization_type == 'Balance Distribution by Churn':
            plot_balance_distribution(data)
        elif visualization_type == 'Geography Distribution':
            plot_categorical_distribution(data, 'Geography')
        elif visualization_type == 'Gender Distribution':
            plot_categorical_distribution(data, 'Gender')
        elif visualization_type == 'NumOfProducts Distribution':
            plot_categorical_distribution(data, 'NumOfProducts')
        elif visualization_type == 'HasCrCard Distribution':
            plot_categorical_distribution(data, 'HasCrCard')



if __name__ == '__main__':
    main()
