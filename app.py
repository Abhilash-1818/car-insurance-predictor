# app.py
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title(" Car Insurance Prediction App")

st.markdown("Fill the customer details to predict if they will buy car insurance.")

# Input form
def user_input_features():
    st.header("Customer Details")

    # Numerical fields
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    balance = st.number_input("Balance", value=1000)
    hh_insurance = st.selectbox("HH Insurance (Home Insurance)", [0, 1])
    car_loan = st.selectbox("Car Loan", [0, 1])
    last_contact_day = st.number_input("Last Contact Day", min_value=1, max_value=31, value=15)
    no_of_contacts = st.number_input("Number of Contacts", value=1)
    days_passed = st.number_input("Days Passed", value=-1)
    prev_attempts = st.number_input("Previous Attempts", value=0)

    # Category maps (you used LabelEncoder previously)
    job_map = {
        "management": 0, "blue-collar": 1, "technician": 2, "admin.": 3,
        "services": 4, "retired": 5, "self-employed": 6, "entrepreneur": 7,
        "unemployed": 8, "housemaid": 9, "student": 10, "unknown": 11
    }
    marital_map = {"single": 0, "married": 1, "divorced": 2}
    education_map = {"primary": 0, "secondary": 1, "tertiary": 2}
    communication_map = {"telephone": 0, "cellular": 1}
    month_map = {
        "jan": 0, "feb": 1, "mar": 2, "apr": 3, "may": 4, "jun": 5,
        "jul": 6, "aug": 7, "sep": 8, "oct": 9, "nov": 10, "dec": 11
    }

    # Show dropdowns with actual names
    job = st.selectbox("Job", list(job_map.keys()))
    marital = st.selectbox("Marital Status", list(marital_map.keys()))
    education = st.selectbox("Education", list(education_map.keys()))
    communication = st.selectbox("Communication Type", list(communication_map.keys()))
    last_contact_month = st.selectbox("Last Contact Month", list(month_map.keys()))

    # Convert selections to numeric codes using maps
    data = {
        'Age': age,
        'Balance': balance,
        'HHInsurance': hh_insurance,
        'CarLoan': car_loan,
        'LastContactDay': last_contact_day,
        'NoOfContacts': no_of_contacts,
        'DaysPassed': days_passed,
        'PrevAttempts': prev_attempts,
        'Job': job_map[job],
        'Marital': marital_map[marital],
        'Education': education_map[education],
        'Communication': communication_map[communication],
        'LastContactMonth': month_map[last_contact_month]
    }

    features = pd.DataFrame([data])
    return features

input_df = user_input_features()

if st.button("Predict"):
    prediction = model.predict(input_df)
    if prediction[0] == 1:
        st.success("This person is likely to buy car insurance.")
    else:
        st.warning("This person is NOT likely to buy car insurance.")
