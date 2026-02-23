import streamlit as st
import pandas as pd
import joblib

import joblib

# Load all models at once
models = joblib.load("best_models.pkl")

rf_model = models["RandomForest"]
dt_model = models["DecisionTree"]
xgb_model = models["XGBoost"]


st.title("Rainfall Prediction App 🌧️")

# Sidebar inputs
st.sidebar.header("Input Weather Data")
pressure = st.sidebar.number_input("Pressure", value=1015.9)
dewpoint = st.sidebar.number_input("Dew Point", value=19.9)
humidity = st.sidebar.number_input("Humidity", value=95)
cloud = st.sidebar.number_input("Cloud Cover", value=81)
sunshine = st.sidebar.number_input("Sunshine", value=40.0)
winddirection = st.sidebar.number_input("Wind Direction", value=13)
windspeed = st.sidebar.number_input("Wind Speed", value=7)

# Create input dataframe
input_df = pd.DataFrame(
    [[pressure, dewpoint, humidity, cloud, sunshine, winddirection, windspeed]],
    columns=['pressure', 'dewpoint', 'humidity', 'cloud', 'sunshine',
             'winddirection', 'windspeed']
)

# Model selection
model_choice = st.selectbox("Select Model", ["Random Forest", "Decision Tree", "XGBoost"])

# Predict button
if st.button("Predict"):
    if model_choice == "Random Forest":
        model = rf_model
    elif model_choice == "Decision Tree":
        model = dt_model
    else:
        model = xgb_model

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    st.write(f"**Prediction:** {'Rainfall' if prediction==1 else 'No Rainfall'}")
    st.write(f"**Probability of No Rainfall:** {probability[0]*100:.2f}%")
    st.write(f"**Probability of Rainfall:** {probability[1]*100:.2f}%")
