# RaceTree

# IMPORTS
import database
import json
import os
import shutil
import sys
from RaceTreeFunctions import *
from RaceTreeFunctions2 import *

# GLOBAL VARIABLES
global sessionDATA


# FOR TESTING - MANUALLY SET SESSION ID
#Session_ID = "9198338"

# PROMPT FOR USER INPUT OF SESSION ID
Session_ID = input("Enter Session ID: ")
print("Confirm Session ID = ", Session_ID)

# SET VARIABLS FOR THE DIFFERENT SECTIONS OF THE WEBSITE TO GET THE DATA FROM
my_base_url = "https://eventresults-api.speedhive.com/api/v0.2.3/eventresults/sessions/"
my_laps = my_base_url + Session_ID + "/lapdata/"
my_classification = my_base_url + Session_ID + "/classification"

# OPEN DATABASE CONNECTION
conn, cursor = database.connect_to_database()
# CHECK IF SESSION DATA IS ALREADY IN DATABASE
query_SessionExists = "SELECT COUNT(1) FROM Laps2 WHERE lapDataInfo_sessionId = ?"

# EXECUTE THE QUERY
cursor.execute(query_SessionExists, (Session_ID,))
result = cursor.fetchone()

# CHECK IF THE SESSION EXISTS
if result[0] > 0:
    print(f"The session already exists in the database.")
    user_input = input("Do you want to update kart numbers? (yes/no): ").strip().lower()
    if user_input == 'yes':
        update_kart_numbers(conn, cursor, Session_ID)
        print("Kart numbers updated.")
        sys.exit()
    else:
        print("Exiting the script.")
        sys.exit()


    
else:
    print(f"The session ID {Session_ID} does not exist in the database.")
    # IF NOT, GET DATA
    # GET & STORE DRIVER INFO FROM MYLAPS
    sessionDATA = get_sessionDATA(my_classification)
    # STORE DRIVER INFO IN DATABASE
    
# GET THE NUMBER OF DRIVERS FROM THE DATABASE
'''
query_NumDrivers = """
    SELECT COUNT(*) 
    FROM (SELECT DISTINCT lapDataInfo_participantInfo_startNr 
          FROM Laps2 
          WHERE lapDataInfo_sessionId = ?)
"""

# EXECUTE THE QUERY
cursor.execute(query_NumDrivers, (Session_ID,))
numDrivers = cursor.fetchone()[0]
'''

##### DEBUG
#numDrivers = fnum_drivers(global_json_data)
numDrivers = fnum_drivers(sessionDATA)
print (type(numDrivers))
print ("numDrivers: " + str(numDrivers))
##### END DEBUG

print ("There are " + str(numDrivers) + " Drivers in this race")

#########################  GET & SAVE LAP DATA #########################################
count = 1
for a in range(1, numDrivers + 1):  # Loop from 1 to numDrivers
    my_laps2 = my_laps + str(a) + "/laps"
    driver_laps_data = function_lap_data(my_laps2)  # Retrieve lap data for the current driver

    count = count + 1
    save_json_data_to_database(conn, cursor, driver_laps_data)  # Save lap data to the database

######################### END GET & SAVE LAP DATA ######################################
############################# CREATE STARTING GRID JSON DATA FOR AE ######################################################

# POPULATE STARTING GRID 
query_01 = """
        SELECT *
        FROM Laps2 AS l
        INNER JOIN (
            SELECT DISTINCT lapDataInfo_participantInfo_startNr, 
                            MIN(lapDataInfo_sessionId) AS sessionId
            FROM Laps2
            WHERE lapDataInfo_sessionId = ? AND lapDataInfo_allLapsHaveFieldPos = true
            GROUP BY lapDataInfo_participantInfo_startNr
        ) AS distinct_laps ON l.lapDataInfo_participantInfo_startNr = distinct_laps.lapDataInfo_participantInfo_startNr
        AND l.lapDataInfo_sessionId = distinct_laps.sessionId
        """
# Fetch all relevant rows
query = """
    SELECT *
    FROM Laps2
    WHERE lapDataInfo_sessionId = ? 
    AND lapDataInfo_allLapsHaveFieldPos = true
"""

cursor.execute(query, (Session_ID,))
rows = cursor.fetchall()

# Dictionary to hold unique drivers based on startNr
unique_drivers = {}
for row in rows:
    start_nr = row.lapDataInfo_participantInfo_startNr
    if start_nr not in unique_drivers:
        unique_drivers[start_nr] = row

# Convert dictionary values to a list to get unique rows
unique_rows = list(unique_drivers.values())

# Sort the unique rows by position
sorted_unique_rows = sorted(unique_rows, key=lambda x: x.lapDataInfo_participantInfo_startPos)

# Function to create grid order
def create_grid_order_json(rows):
    starting_grid = []
    for row in rows:
        grid_entry = {
            "position": row.lapDataInfo_participantInfo_startPos,
            "name": row.lapDataInfo_participantInfo_name,
            "kartNumber": row.lapDataInfo_participantInfo_startNr
        }
        starting_grid.append(grid_entry)
    return {"startingGrid": starting_grid}

# Create JSON data with sorted rows
starting_grid_data = create_starting_grid_json(sorted_unique_rows)

# Now you can use the starting_grid_data as needed
#print("starting grid data" + str(starting_grid_data))


with open("Starting_Grid.json", 'w') as file:
    json.dump(starting_grid_data, file, indent=4)

print ("Starting Grid JSON file created")


########################   END STARTING GRID JSON DATA  #########################################################

########################  GET STARTING TOD FROM DATABASE  #######################################################

query_TOD = '''
    SELECT *
    FROM Laps2
    WHERE lapDataInfo_sessionID = ? AND laps_lapNr = ?
    ORDER BY lapDataInfo_participantInfo_startPos
'''
# Assuming conn is your connection object
my_lap_number = 1 # default number just to get the instance
cursor.execute(query_TOD, (Session_ID, 1))
# Fetch the results
rows = cursor.fetchall()
# call function to create json data
start_time = calc_start_TOD(rows)
adjustment_time = start_time # - 60 # enable the 60 seconds later

print("my adjustment is: " + str(start_time))

###########################  END STARTING TOD  ####################################################

###########################  GET LAP DATA  ####################################

#get the grid order
grid_order = starting_grid_data

#Get the number of laps
query_numLaps = '''
    SELECT lapDataInfo_lapCount
    FROM Laps2
    WHERE lapDataInfo_sessionID = ? 
'''
# Assuming conn is your connection object
cursor.execute(query_numLaps, (Session_ID))
# Fetch the results
rows = cursor.fetchall()

num_laps = rows[0][0] + 1

print("there are " + str(num_laps) +  " laps in this race")


# Initialize a variable to store the accumulated JSON data
all_lap_data = []

#loop through each lap to populate the json data
query_01 = '''
    SELECT *
    FROM Laps2
    WHERE lapDataInfo_sessionID = ? AND laps_lapNr = ?
    ORDER BY laps_fieldComparison_position
'''
with open("LapData.json", 'w') as file:
    print ("LapData.json file created")


# Define the folder path
laps_folder = "Laps"

# Check if the folder exists
if os.path.exists(laps_folder):
    # Delete the folder and all its contents
    shutil.rmtree(laps_folder)

# Recreate the folder
os.makedirs(laps_folder)

#write the number of laps to a file for javascript to read later.
lap_num_file = "lapNumFile.txt"
with open(lap_num_file, 'w') as file:
    file.write(str(num_laps-1))

for i in range(1, num_laps):
    my_lap_number = i

    # Assuming conn is your connection object
    cursor.execute(query_01, (Session_ID, my_lap_number))

    # Fetch the results
    rows = cursor.fetchall()

    #//print ("GridOrderIndex: " + grid_order.index(kartnumber))

    # Call function to create JSON data for the lap
    #print("calling create_lap_data()")
    lap_data, grid_order = create_lap_data(rows, adjustment_time, grid_order, my_lap_number)

    # Create filename for the lap data inside the "Laps" folder
    lap_filename = os.path.join(laps_folder, f"Lap_{my_lap_number}.json")

    # Write the lap data to its own file inside the "Laps" folder
    with open(lap_filename, 'w') as file:
        json.dump(lap_data, file, indent=4)








