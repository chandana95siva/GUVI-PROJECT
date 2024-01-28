import streamlit as st
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore")
# Set page title and favicon
st.set_page_config(page_title="SG Resale Flat Predictor", page_icon="🏡")

# Define the content for the homepage
def homepage():
    # Use HTML and inline CSS to set the color of the header
    st.markdown(
        """
        <style>
            .title-text {
                color: #3498db;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.header("Singapore Resale Flat Prices Predictor")

    st.image("singapore.jpeg", caption="Image Source: Unsplash", use_column_width=True)

    st.write(
        "Welcome to the Singapore Resale Flat Prices Predictor! This web application is designed to help you estimate the resale value of flats in Singapore based on historical data of resale transactions."
    )

    st.markdown("### Project Skills Takeaway:")
    st.write("- Data Wrangling")
    st.write("- Exploratory Data Analysis (EDA)")
    st.write("- Model Building")
    st.write("- Model Deployment")

    st.markdown("### How to Use:")
    st.write("1. Navigate to the 'Predict' section from the sidebar.")
    st.write("2. Enter the required details about the flat.")
    st.write("3. Click the 'Predict' button to get the estimated resale price.")

    st.markdown("### Why Use This Predictor?")
    st.write(
        "Whether you are a potential buyer or seller, this predictor aims to provide you with a quick and reliable estimate of the resale value of a flat, helping you make informed decisions in the real estate market."
    )

    st.markdown("### Get Started")


# Create a sidebar for navigation
def sidebar():
    st.sidebar.title("Navigation")
    selected_option = st.sidebar.radio("Go to", ["Home", "Predict"])

    if selected_option == "Home":
        homepage()
    elif selected_option == "Predict":

            # Load the trained model
        with open('Singapore_resale_price.pkl', 'rb') as f:
            model = pickle.load(f)


        # Create the Streamlit app
        def main():
            st.title('Resale Price Prediction')

            with st.form("prediction_form"):
                # User inputs
                floor_area_sqm = st.number_input('Floor Area (sqm):', value=4.55)
                flat_type_mapping = {'4 ROOM': 0, '3 ROOM': 1, '5 ROOM': 2, 'EXECUTIVE': 3, '2 ROOM': 4, '1 ROOM': 5, 'MULTI GENERATION': 6}
                flat_type = st.selectbox('Flat Type:', list(flat_type_mapping.keys()), index=0)
                lease_remain_years = st.number_input('Lease Remain Years:', value=69.97)
                lease_commence_date = st.date_input('Lease Commence Date:', pd.to_datetime('1994-12-22'))
                storey_range_mapping = {'10 TO 12': 0, '04 TO 06': 1, '07 TO 09': 2, '01 TO 03': 3, '13 TO 15': 4, '19 TO 21': 5, '16 TO 18': 6,
                                        '25 TO 27': 7, '22 TO 24': 8, '28 TO 30': 9, '31 TO 33': 10, '40 TO 42': 11, '37 TO 39': 12, '34 TO 36': 13,
                                        '46 TO 48': 14, '43 TO 45': 15, '49 TO 51': 16, '06 TO 10': 17, '01 TO 05': 18, '11 TO 15': 19, '16 TO 20': 20,
                                        '21 TO 25': 21, '26 TO 30': 22, '36 TO 40': 23, '31 TO 35': 24}
                storey_range = st.selectbox('Storey Range:', list(storey_range_mapping.keys()), index=0)
                year = st.number_input('Year:', value=2019)
                storey_median = st.number_input('Storey Median:', value=1.93)
                is_new_options = [0, 1]  # Assuming binary values for 'Is New'
                is_new = st.selectbox('Is New:', is_new_options, index=0)
                high_floor_options = [0, 1]  # Assuming binary values for 'High Floor'
                high_floor = st.selectbox('High Floor:', high_floor_options, index=0)
                flat_model_mapping = {'MODEL A': 0, 'IMPROVED': 1, 'NEW GENERATION': 2, 'SIMPLIFIED': 3, 'PREMIUM APARTMENT': 4, 'STANDARD': 5,
                                    'APARTMENT': 6, 'MAISONETTE': 7, 'MODEL A2': 8, 'DBSS': 9, 'MODEL A-MAISONETTE': 10, 'ADJOINED FLAT': 11,
                                    'TERRACE': 12, 'MULTI GENERATION': 13, 'TYPE S1': 14, 'TYPE S2': 15, 'IMPROVED-MAISONETTE': 16, '2-ROOM': 17,
                                    'PREMIUM APARTMENT LOFT': 18, 'PREMIUM MAISONETTE': 19, '3GEN': 20}
                flat_model = st.selectbox('Flat Model:', list(flat_model_mapping.keys()), index=0)
                price_per_sqm = st.number_input('Price per sqm:', value=2.87)

                # Submit button for prediction
                submit_button = st.form_submit_button("Predict Average Resale Price")

            if submit_button:
                # Convert categorical variables to numeric representations
                flat_type_numeric = flat_type_mapping.get(flat_type, 0)
                storey_range_numeric = storey_range_mapping.get(storey_range, 0)
                flat_model_numeric = flat_model_mapping.get(flat_model, 0)

                # Create input data DataFrame
                input_data = {
                    'floor_area_sqm': floor_area_sqm,
                    'flat_type': flat_type_numeric,
                    'lease_remain_years': lease_remain_years,
                    'lease_commence_date': lease_commence_date.year,
                    'storey_range': storey_range_numeric,
                    'year': year,
                    'storey_median': storey_median,
                    'is_new': is_new,
                    'high_floor': high_floor,
                    'flat_model': flat_model_numeric,
                    'price_per_sqm': price_per_sqm
                }
                input_df = pd.DataFrame([input_data])

                # Make prediction
                predicted_prices = model.predict(input_df)
                average_price = predicted_prices.mean()

                st.success(f'Average Predicted Resale Price: {average_price:.2f}')

        main()

    # Display the sidebar and homepage
sidebar()

