#!/bin/bash



# Execute the Streamlit app script in the background
streamlit run NotOnTime_Trips_Dashboard.py &

# Open the Streamlit app in the default web browser
sleep 50  # Wait for Streamlit to start (adjust the time if needed)

# Open the app in a web browser 
open http://localhost:8501
