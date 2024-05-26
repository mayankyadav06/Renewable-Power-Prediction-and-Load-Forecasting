import streamlit as st
import pandas as pd
import pickle
import base64
import sklearn
import xgboost


# Load the models
with open("solar_rf.pkl","rb") as file:
    solar_model = pickle.load(file)

with open("load_xgb_model.pkl","rb") as file:
    load_model = pickle.load(file)
# Using the older version of XGBoost

with open("wind_rf.pkl","rb") as file:
    wind_model = pickle.load(file)



# Define a function to make predictions
def make_prediction(model, input_data, feature_names):
    input_df = pd.DataFrame([input_data], columns=feature_names)
    prediction = model.predict(input_df)
    return prediction

# Create the Streamlit app
def app():
    # Set the page config to wide mode
    st.set_page_config(layout="wide")
    # Initialize session state if it doesn't exist
    if 'solar_prediction' not in st.session_state:
        st.session_state['solar_prediction'] = None
    if 'load_prediction' not in st.session_state:
        st.session_state['load_prediction'] = None
    if 'wind_prediction' not in st.session_state:
        st.session_state['wind_prediciton'] = None

    # Define the style for the background image
    main_bg = "img2.jpeg"
    main_bg_ext = "jpg"

    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('Solar Power and Load Forecasting')

    # Create two columns for the inputs
    col1, col2 = st.columns(2)

    with col1:
        st.header('Solar Power Prediction')
        # User inputs
        global_solar_incidence = st.text_input("Enter Global Solar Incidence",key="global_solar_incidence",value="0.0")
        global_solar_incidence = float(global_solar_incidence) 

        
        solar_altitude = st.text_input("Enter Solar Altitude",key="solar_altitude",value="0.0")
        solar_altitude = float(solar_altitude)

        solar_azimuth_angle = st.text_input("Enter Solar Azimuth Angle", key="solar_azimuth",value="0.0")
        solar_azimuth_angle = float(solar_azimuth_angle) 

        solar_angle_of_incidence = st.text_input("Enter Solar Angle of Incidence",key="solar_incidence_angle",value="0.0")
        solar_angle_of_incidence = float(solar_angle_of_incidence) 

        solar_cell_temp = st.text_input("Enter Solar Cell Temperature",key="solar_cell_temp",value="0.0")
        solar_cell_temp = float(solar_cell_temp) 

        solar_insolation = st.text_input("Enter Solar Insolation",key="solar_insolation",value="0.0")
        solar_insolation = float(solar_insolation) 

        year = st.text_input("Enter Year",key="solar_year",value="0")
        year = int(year) 

        month = st.text_input("Enter Month",key="solar_month",value="0")
        month = int(month) 

        day = st.text_input("Enter Day",key="solar_day",value="0")
        day = int(day) 

        hour = st.text_input("Enter Hour",key="solar_hour",value="0")
        hour = int(hour) 

        # When the 'Predict' button is clicked, make the prediction and display it
        if st.button('Predict Solar Power',key ="solar_prediciton_button"):
            input_data = (global_solar_incidence, solar_altitude, solar_azimuth_angle, solar_angle_of_incidence, solar_cell_temp, solar_insolation, year, month, day, hour)
            st.session_state['solar_prediction'] = make_prediction(solar_model, input_data, ['Global Solar', 'Solar Altitude', 'Solar Azimuth', 'Solar Angle of Incidence', 'Solar Cell Temperature', 'Solar Insolation', 'Year', 'Month', 'Day', 'Hour'])
            st.write('The predicted solar power output is (KW):', st.session_state['solar_prediction'])


    with col2:
        st.header('Load Forecasting')
        # User inputs
        ac_primary_load = st.text_input("Enter AC Primary Load",key="ac_primary_load",value="0.0")
        ac_primary_load = float(ac_primary_load) 

        ac_primary_load_served = st.text_input("Enter AC Primary Load Served",key="ac_primary_load_served",value="0.0")
        ac_primary_load_served = float(ac_primary_load_served) 

        unmet_electrical_load = st.text_input("Enter Unmet Electrical Load", key="unmet_elec_load",value="0.0")
        unmet_electrical_load = float(unmet_electrical_load) 

        year_input = st.text_input("Enter Year", key="load_year",value="0")
        year = int(year_input) 

        month = st.text_input("Enter Month", key="load_month",value="0")
        month = int(month) 

        day = st.text_input("Enter Day", key="load_day",value="0")
        day = int(day)   

        hour = st.text_input("Enter Hour", key="load_hour",value="0")
        hour = int(hour) 

        minute = st.text_input("Enter Minute", key="load_minute",value="0")
        minute = int(minute) 

        # When the 'Predict Load' button is clicked, make the prediction and store it in session state
        if st.button('Predict Load',key="load_prediciton_button"):
            input_data = (ac_primary_load, ac_primary_load_served, unmet_electrical_load, year, hour, month, minute, day)
            st.session_state['load_prediction'] = make_prediction(load_model, input_data, ['AC Primary Load', 'AC Primary Load Served', 'Unmet Electrical Load', 'Year', 'Hour', 'Month', 'Minute', 'Day'])
            st.write('The forecasted load value is (KW):', st.session_state['load_prediction'])

    if st.button("Wind"):
        st.header('Wind Power Prediction')
        # User inputs
        ambient_temperature = st.text_input("Enter Ambient Temperature",key="ambient_temp",value="0.0")
        ambient_temperature = float(ambient_temperature) 

        wind_speed = st.text_input("Enter Wind Speed",key="wind_speed",value="0.0")
        wind_speed = float(wind_speed)

        wind_turbine_status = 0

        year = st.text_input("Enter Year",key="wind_year",value="0")
        year = int(year) 

        month = st.text_input("Enter Month",key="wind_month",value="0")
        month = int(month) 

        day = st.text_input("Enter Day",key="wind_day",value="0")
        day = int(day) 

        hour = st.text_input("Enter Hour",key="wind_hour",value="0")
        hour = int(hour) 

        # When the 'Predict' button is clicked, make the prediction and display it
        if st.button('Predict Wind Power',key ="wind_prediction_button"):
            input_wind_data = (ambient_temperature, wind_speed, wind_turbine_status, year, month, day, hour)
            st.session_state['wind_prediction'] = make_prediction(wind_model, input_wind_data, ['Ambient Temperature', 'Wind Speed', 'Wind turbine Operating Status', 'Year', 'Month', 'Day', 'Hour'])
            st.write('The predicted wind power output is (KW):', st.session_state['wind_power'])


    if st.button("Sugsestions"):
        st.balloons()
        
        if st.session_state['solar_prediction'] is None or st.session_state['load_prediction'] is None:
            st.write("Predict Load and Solar Power Output first....")
            exit

        elif st.session_state['solar_prediction'] - st.session_state['load_prediction'] < st.session_state['solar_prediction']:
            unmet_load = st.session_state['load_prediction'] - st.session_state['solar_prediction']
            if unmet_load <= 30:
                cost_from_grid = unmet_load * 3.34
            elif unmet_load > 30 and unmet_load <= 50:
                cost_from_grid = unmet_load * 4.37
            elif unmet_load >= 51 and unmet_load <= 150:
                cost_from_grid = unmet_load * 5.23
            elif unmet_load >= 151 and unmet_load <= 300:
                cost_from_grid = unmet_load * 6.61
            elif unmet_load > 300:
                cost_from_grid = unmet_load * 6.80

            st.write("You can take the required power KW", unmet_load,"from MP electricity grid with the price of Rs.",cost_from_grid)

        elif st.session_state['solar_prediction'] - st.session_state['load_prediction'] > st.session_state['solar_prediction']:

            st.write("You can sell your excess generation to Grid")

if __name__ == '__main__':
    app()