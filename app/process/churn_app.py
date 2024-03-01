import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle

# Charger le modele
rfcmodel=pickle.load(open('model/rfcmodel.pkl','rb'))
scalar=pickle.load(open('model/scaling.pkl','rb'))

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
    output=rfcmodel.predict(new_data)
    print('Output du model => {}'.format(output[0]))
    return output

# Streamlit interface
def main():
    st.title('Churn Prediction')
    st.image('Images/Customer-Churn.png', use_column_width='auto')

    st.sidebar.title('Taux de désabonnement des clients ??')
    st.sidebar.image('Images/graphic.png')
    st.sidebar.info(
        """
    Le présent modèle d’apprentissage automatique estcapable de prédire si les clients d’une banque quittent ou non la banque.

        """
    )
    
    # Load the dataset
    file_path = 'app/data/churn.csv'  # Replace with the path to your dataset
    data = load_data(file_path)

    # User input for features
    credit_score = st.slider('Credit Score', min_value=300, max_value=850, step=1, value=500)
    age = st.slider('Age', min_value=18, max_value=100, step=1, value=30)
    balance = st.number_input('Balance', min_value=0.0, step=1.0, value=0.0)
    num_of_products = st.slider('Number of Products', min_value=1, max_value=4, step=1, value=1)
    estimated_salary = st.number_input('Estimated Salary', min_value=0.0, step=1.0, value=50000.0)
    tenure = st.slider('Tenure (in years)', min_value=0, max_value=20, step=1, value=5)
    is_active_member = st.radio('Is Active Member?', ('Yes', 'No'))
    has_cr_card = st.radio('Has Credit Card?', ('Yes', 'No'))
    geography = st.selectbox('Geography', ('France', 'Germany', 'Spain'))
    gender = st.selectbox('Gender', ('Female', 'Male'))

    # Map radio button responses to binary values
    is_active_member = 1 if is_active_member == 'Yes' else 0
    has_cr_card = 1 if has_cr_card == 'Yes' else 0
    if geography == 'France':
        geography = 0
    elif geography == 'Germany':
        geography = 1
    else:
        geography = 2
    
    gender = 1 if gender == 'Mal' else 0


    input_data = {'CreditScore': credit_score,
                  'Age': age,
                  'Balance': balance,
                  'NumOfProducts': num_of_products,
                  'EstimatedSalary': estimated_salary,
                  'Tenure': tenure,
                  'IsActiveMember': is_active_member,
                  'HasCrCard': has_cr_card,
                  'Geography': geography,
                  'Gender': gender}

    # When the user clicks the predict button
    if st.button('Predict'):
        # Make prediction
        prediction = preprocess_data(input_data)
        # Display prediction result
        if prediction[0] == 0:
            st.success('Customer is predicted to stay.')
        else:
            st.warning('Customer is predicted to churn.')

    # Data visualization
    st.header('Data Visualization')

    # Churn Distribution
    st.subheader('Churn Distribution')
    st.bar_chart(data['Exited'].value_counts())

    # Age Distribution by Churn
    st.subheader('Age Distribution by Churn')
    fig, ax = plt.subplots()
    sns.histplot(data=data, x='Age', hue='Exited', kde=True, multiple='stack', ax=ax)
    st.pyplot(fig)

    # Balance Distribution by Churn
    st.subheader('Balance Distribution by Churn')
    fig, ax = plt.subplots()
    sns.histplot(data=data, x='Balance', hue='Exited', kde=True, multiple='stack', ax=ax)
    st.pyplot(fig)

    # Distribution of 'Geography'
    st.subheader('Distribution of Geography')
    st.bar_chart(data['Geography'].value_counts())

    # Distribution of 'Gender'
    st.subheader('Distribution of Gender')
    st.bar_chart(data['Gender'].value_counts())

    # Distribution of 'NumOfProducts'
    st.subheader('Distribution of Number of Products')
    st.bar_chart(data['NumOfProducts'].value_counts())

    # Distribution of 'HasCrCard'
    st.subheader('Distribution of Has Credit Card')
    st.bar_chart(data['HasCrCard'].value_counts())

if __name__ == '__main__':
    main()
