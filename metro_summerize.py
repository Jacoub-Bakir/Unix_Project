import json
import os
import datetime
from pymongo import MongoClient

# Function to process each Siri record
def process_siri_record(data, collection):
    not_on_time_trips = {}
    for record in data:
        for delivery in record['Siri']['ServiceDelivery']['StopMonitoringDelivery']:
            for visit in delivery['MonitoredStopVisit']:
                line_ref = visit['MonitoredVehicleJourney']['LineRef']['value']
                journey_ref = visit['MonitoredVehicleJourney']['FramedVehicleJourneyRef']['DatedVehicleJourneyRef']
                departure_status = visit['MonitoredVehicleJourney']['MonitoredCall']['DepartureStatus']
                monitored_call = visit['MonitoredVehicleJourney']['MonitoredCall']

                # Get the time field based on priority: ExpectedDepartureTime -> ExpectedArrivalTime -> RecordedAtTime
                if 'ExpectedDepartureTime' in monitored_call:
                    time_field = monitored_call['ExpectedDepartureTime']
                elif 'ExpectedArrivalTime' in monitored_call:
                    time_field = monitored_call['ExpectedArrivalTime']
                else:
                    time_field = visit['RecordedAtTime']

                # Extract date from the time field
                date_from_time_field = datetime.datetime.strptime(time_field, "%Y-%m-%dT%H:%M:%S.%fZ").date()

                # Combine LineRef and Date to create a unique key
                key = (line_ref, date_from_time_field)

                # Initialize or update the not_on_time_trips dictionary
                if key not in not_on_time_trips:
                    not_on_time_trips[key] = set()

                if departure_status != 'onTime':
                    not_on_time_trips[key].add(journey_ref)

    # Store results in MongoDB
    for key, journeys in not_on_time_trips.items():
        line_ref, date = key
        document = {
            'LineRef': line_ref,
            'Date': datetime.datetime.combine(date, datetime.datetime.min.time()),
            'NotOnTimeCount': len(journeys)
        }
        collection.insert_one(document)

# Directory containing JSON files
json_dir = 'retrieved_data/metro_next_departures'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['TransportationHub']
collection = db['Metro']

# Accumulate all Siri records from multiple JSON files
all_siri_records = []
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(json_dir, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            all_siri_records.extend(data)

# Process all Siri records and save results to MongoDB
process_siri_record(all_siri_records, collection)

print("Data saved to MongoDB.")
