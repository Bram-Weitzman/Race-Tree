#Imports
from myFunctions import *
from myFunctions import f_close_DB
import myFunctions
import json
import database
import Main


SessionID = "8188741"
################################### OPEN DB CONNECTION ##################################

database.connect_to_database()
cursor = database.conn.cursor()

#########################################################################################

import json

# Create an empty dictionary to store lap data
lap_data = {}

# Create a dictionary to store the fastest lap time for each lap
fastest_lap_times = {}

# Initialize overall fastest lap time to infinity
overall_fastest_lap_time = float('inf')

# Loop through laps from 1 to 24
for lap_number in range(1, 25):
    lap_data[lap_number] = []  # Initialize an empty list for each lap

    # Execute the SQL query to fetch data for the current lap (lap_number) and the previous lap (lap_number - 1)
    cursor.execute(f"""
        SELECT L.DriverID, D.driver_name, L.Lap{lap_number}TOD, L.Lap{lap_number - 1}TOD
        FROM Laps AS L 
        INNER JOIN Drivers AS D ON L.DriverID = D.ID
        WHERE L.SessionID = ? 
        ORDER BY L.Lap{lap_number}TOD ASC
    """, (SessionID,))

    # Fetch all rows
    rows = cursor.fetchall()

    # Check if any rows were fetched
    if rows:
        # Append data for each row to the lap data dictionary
        for row in rows:
            driver_id, driver_name, cur_lap_tod, prev_lap_tod = row
            # Check to make sure lap time exists
            if cur_lap_tod > 0 and prev_lap_tod > 0:
                # Calculate lap time
                lap_time = cur_lap_tod - prev_lap_tod
                # Append driver ID, driver name, current lap TOD, previous lap TOD, and lap time to the current lap's data list
                lap_data[lap_number].append({
                    "driver_id": driver_id,
                    "driver_name": driver_name,
                    "cur_lap_tod": cur_lap_tod,
                    "prev_lap_tod": prev_lap_tod,
                    "lap_time": lap_time
                })

                # Update the overall fastest lap time if the current lap time is faster
                if lap_time < overall_fastest_lap_time:
                    overall_fastest_lap_time = lap_time

    else:
        print(f"No data found for Lap {lap_number}")

    # Store the fastest lap time for the current lap
    fastest_lap_times[lap_number] = overall_fastest_lap_time

# Loop through lap data to mark the fastest lap of each driver as purple if it's the fastest lap of the race
for lap_number, lap_info in lap_data.items():
    for lap in lap_info:
        if lap["lap_time"] == fastest_lap_times[lap_number]:
            lap["color"] = "purple"

# Write the lap data to a JSON file
with open("lap_data.json", "w") as json_file:
    json.dump(lap_data, json_file, indent=4)

print("JSON data file created successfully.")












################################### Close DB CONNECTION ##################################

database.close_database_connection()
 
#########################################################################################




