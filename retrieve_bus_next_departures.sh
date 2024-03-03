#!/bin/bash

# Define the URL for fetching next departures data from the API
API_URL="https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring"
API_KEY="LLEPeOBTiXI8AoFAful1FPQquZCUrmO9"
# Define the path to the text file containing stops IDs
STOPS_FILE="/Users/mac/Desktop/ParisCité_M1/Adm_Linux/project/updates/bus_ids.txt"

# Define the directory to store the output file
OUTPUT_DIR="/Users/mac/Desktop/ParisCité_M1/Adm_Linux/project/retrieved_data/bus_next_departures"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Generate filename based on date and time
FILENAME="$OUTPUT_DIR/$(date +'%Y%m%d_%H%M%S').json"

# Initialize an empty array to store all next departures
NEXT_DEPARTURES=()

# Loop through each stop ID in the text file
while IFS= read -r stopArea_id; do

    # Remove any leading or trailing whitespace
    stopArea_id=$(echo "$stopArea_id" | xargs)

    # Fetch next departures for the current stop and append to the array (StopPoint:Q,StopArea:SP)
    next_departures=$(curl -sf "${API_URL}?MonitoringRef=STIF:StopArea:SP:${stopArea_id}:" -H "apikey: ${API_KEY}" 2>&1)

    if [ $? -eq 0 ]; then
        NEXT_DEPARTURES+=("$next_departures")
    else
        echo "Error fetching data for stop $stopArea_id" >&2
    fi
done < "$STOPS_FILE"

# Convert the array to JSON format
next_departures_json=$(printf '%s\n' "${NEXT_DEPARTURES[@]}" | jq -s '.' --exit-status)

# Check if jq encountered an error
if [ $? -eq 0 ]; then
    # Save the next departures data to the output file
    echo "$next_departures_json" > "$FILENAME"
    echo "Next departures data saved to $FILENAME"
else
    echo "Error processing JSON data" >&2
fi
