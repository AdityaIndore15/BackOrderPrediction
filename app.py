import streamlit as st
import pandas as pd
import joblib

# Load the model and preprocessing components
model = joblib.load(r"D:\\BackOrderPrediction\\random_forest_model.pkl")
label_encoders = joblib.load(r"D:\\BackOrderPrediction\\label_encoders.pkl")
target_encoder = joblib.load(r"D:\\BackOrderPrediction\\target_encoder.pkl")
scaler = joblib.load(r"D:\\BackOrderPrediction\\scaler.pkl")

# Define the numerical and categorical features
numerical_features = ['forecast_3_month', 'national_inv', 'sales_3_month', 'sales_9_month', 'perf_6_month_avg',
                      'in_transit_qty', 'min_bank', 'lead_time', 'local_bo_qty', 'pieces_past_due']
categorical_features = ['potential_issue', 'ppap_risk', 'deck_risk', 'stop_auto_buy']

# Function to preprocess input data
def preprocess_input(data):
    # Encode categorical features
    for feature in categorical_features:
        le = label_encoders[feature]
        data[feature] = le.transform(data[feature])

    # Standardize numerical features
    data[numerical_features] = scaler.transform(data[numerical_features])

    return data

# Streamlit App
def main():
    st.title("Back Order Prediction")

    # Input Form
    with st.form("prediction_form"):
        st.write("Enter the details for prediction:")

        # Numerical Inputs
        numerical_inputs = {}
        for feature in numerical_features:
            numerical_inputs[feature] = st.number_input(feature.replace('_', ' ').capitalize(), value=0.0)

        # Categorical Inputs
        categorical_inputs = {}
        for feature in categorical_features:
            le = label_encoders[feature]
            categorical_inputs[feature] = st.selectbox(feature.replace('_', ' ').capitalize(), le.classes_)

        # Submit Button
        submit = st.form_submit_button("Predict")

    if submit:
        # Create a DataFrame from the input data
        input_data = pd.DataFrame([numerical_inputs | categorical_inputs])

        # Preprocess the input data
        preprocessed_data = preprocess_input(input_data.copy())

        # Make prediction
        prediction = model.predict(preprocessed_data)
        prediction_label = target_encoder.inverse_transform(prediction)[0]

        result = "The Order Went On BackOrder" if prediction_label == "Yes" else "The Order Did Not Go On BackOrder"
        color = "red" if prediction_label == "Yes" else "green"

        # Display Result
        st.markdown(f"<h2 style='color: {color};'>{result}</h2>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
