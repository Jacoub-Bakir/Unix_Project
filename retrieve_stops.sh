#!/bin/bash

# Define the API URL
API_URL='https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/arrets/exports'
API_KEY="3eca850c74d8c7d78a14e60c4651737beaddb69828b6cdae8d9d2b69"

# Define the directory to store the CSV file
CSV_DIR="/Users/mac/Desktop/ParisCité_M1/Adm_Linux/project/updates"

# Create the directory if it doesn't exist
mkdir -p "$CSV_DIR"

# Download the CSV file
curl -s -o "$CSV_DIR/stops.csv" "$(curl -s "$API_URL" -H "apikey: ${API_KEY}" | jq -r '.links[] | select(.rel == "csv") | .href')"

# Check if the CSV file was downloaded successfully
if [ -f "$CSV_DIR/stops.csv" ]; then
    # Define the path to the Python script
    PYTHON_SCRIPT="extract_stops.py"

    # Run the Python script
    python3 "$PYTHON_SCRIPT"
else
    echo "Failed to download CSV file"
fi
