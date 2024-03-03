import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["TransportationHub"]
metro_collection = db["Metro"]
bus_collection = db["Bus"]
tram_collection = db["Tram"]
rail_collection = db["Rail"]

# Function to fetch data from MongoDB
def fetch_data():
    metro_cursor = metro_collection.find({}, {"_id": 0})  # Exclude _id field
    bus_cursor = bus_collection.find({}, {"_id": 0})  # Exclude _id field
    tram_cursor = tram_collection.find({}, {"_id": 0})  # Exclude _id field
    rail_cursor = rail_collection.find({}, {"_id": 0})  # Exclude _id field
    metro_data = list(metro_cursor)
    bus_data = list(bus_cursor)
    tram_data = list(tram_cursor)
    rail_data = list(rail_cursor)
    combined_data = metro_data + rail_data + bus_data + tram_data
    return combined_data

# Function to preprocess data
def preprocess_data(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Function to group data by date and calculate total not on-time trips
def group_by_date(df):
    grouped = df.groupby('Date').sum()
    return grouped

# Main function to create and run the Streamlit app
def main():
    st.title('Not On-Time Trips Time Series Dashboard')
    
    # Fetch data from MongoDB
    data = fetch_data()
    
    # Preprocess data
    df = preprocess_data(data)
    
    # Group data by date
    grouped_data = group_by_date(df)
    
    # Display time series plot
    st.line_chart(grouped_data['NotOnTimeCount'])

# Run the Streamlit app
if __name__ == '__main__':
    main()
