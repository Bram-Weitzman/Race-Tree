#####################################################################################################
#############################    PYTHON FUNCTIONS    ################################################
#####################################################################################################



#####################################################################################################
#############################   IMPORTS    ##########################################################
import pyodbc
import sys

###########################   END IMPORTS   #########################################################
#####################################################################################################



#####################################################################################################
########################## CREATE STARTING GRID #####################################################

def create_starting_grid_json(rows):
    starting_grid_data = {"startingGrid": []}
    for row in rows:
        # Accessing elements of each tuple by index
        name = row[1]  # Assuming lapDataInfo_name is at index 3
        start_nr = row[5]  # Assuming lapDataInfo_startNr is at index 5
        curr_pos = row[6]  # Assuming lapDataInfo_startPos is at index 6
        
        # Creating a dictionary for each row
        driver_data = {
            "position": curr_pos,
            "name": name,
            "kartNumber": start_nr
            
        }
        starting_grid_data["startingGrid"].append(driver_data)
    
    return starting_grid_data


#########################  END CREATE STARTING GRID #################################################
#####################################################################################################


#####################################################################################################
###########################  GET LAP DATA ###########################################################

def function_lap_data(xhr_url):

    global global_json_data3
    
    import json
    import requests
    #print (xhr_url)



    # Define request headers
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://speedhive.mylaps.com',
        'Referer': 'https://speedhive.mylaps.com/',
        'Sec-Ch-Ua': '\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '\"Windows\"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    # Send GET request to the URL with defined headers
    response = requests.get(xhr_url, headers=headers)
    #print ("xhr_url = " + xhr_url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        json_data = response.json()
        # Write the JSON data to a file with each item on a separate line
        with open('ALL_response_data3.json', 'w') as f:
            json.dump(json_data, f, indent=4)
            global_json_data3= json_data

        return global_json_data3
    else:
        print ("idk")
        

###########################  END GET LAP DATA #######################################################
#####################################################################################################


#####################################################################################################
###########################  DATABASE CONNECTION ####################################################

def f_connect_DB():
    try:
        # Connect to the Access database
        conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=F:\AE Scripts\GetData\myDB.accdb;'
        conn = pyodbc.connect(conn_str)

        # Create a cursor object
        cursor = conn.cursor()

        print("Database connection established successfully.")
        return conn, cursor

    except pyodbc.Error as e:
        print("Error connecting to the database:", e)

    return None, None

def f_close_DB(conn):
    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()

######################## END DATABASE CONNECTIONS ####################################################
######################################################################################################
    


######################################################################################################    
#############################  GET DRIVER INFO  ######################################################
def get_driver_info(xhr_url):

    global global_json_data
    
    import json
    import requests
    #print (xhr_url)



    # Define request headers
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://speedhive.mylaps.com',
        'Referer': 'https://speedhive.mylaps.com/',
        'Sec-Ch-Ua': '\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '\"Windows\"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    # Send GET request to the URL with defined headers
    response = requests.get(xhr_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        json_data = response.json()
        global_json_data = response.json()
        #return global_json_data
        #print (json.dumps(json_data, indent=4))

        # Write the JSON data to a file with each item on a separate line
        with open('ALL_response_data2.json', 'w') as f:
            json.dump(json_data, f, indent=4)

        print("JSON data written to response_data.json")
        return global_json_data
    else:
        print(f"Failed to retrieve JSON data. Status code: {response.status_code}")



#########################  END GET DRIVER INFO ########################################################
#######################################################################################################
        


#######################################################################################################        
############################# CHECK DATABASE FOR EXISTING LAP DATA ####################################

    # Define the SQL statement to check for duplicates
def sql_check_laps(SessionID, conn, cursor):

    Session_booleon = False
    sql_check_duplicate = '''
    SELECT COUNT(*) FROM Laps WHERE SessionID = ? 
    '''
    # Execute the SQL statement to check for duplicates
    cursor.execute(sql_check_duplicate, (SessionID))
    result = cursor.fetchone()
    #If data exists, set the booleon to true
    Session_booleon = result[0] > 0
    
    print ("SessionID is: ", SessionID)
    print("There is data: ", Session_booleon)
    return Session_booleon


############################ END LAP DATA DATABASE CHECK  ############################################
######################################################################################################  



######################################################################################################
########################### SAVE LAPS IN DATABASE ####################################################
def save_json_data_to_database(conn, cursor, json_data):
    try:

        # Extract lap data info
        lap_data_info = json_data["lapDataInfo"]
        session_id = lap_data_info["sessionId"]

        # Iterate through each lap in the "laps" list
        for lap in json_data["laps"]:
            # Extract lap information
            lap_nr = lap["lapNr"]
            time_of_day = lap["timeOfDay"]
            #####################################
            ############  Debug  #################
            # Extract the "name" field from the JSON data
            #participant_name = json_data['lapDataInfo']['participantInfo']['name']
            #participant_startPos = json_data['lapDataInfo']['participantInfo']['startPos']
            # Print the name
            #print("Participant Name:", participant_name)
            #print("Starting Position: ", participant_startPos)
            #######################################            

            # Check if letter at end of kart number
            # This is used for Ontario Interclub races where competitors from different clubs have the same number
            #kartNumber = json_data['lapDataInfo']['participantInfo']['startnNr']
            #print ("Kart Number: " + kartNumber)

            # Check if the record already exists in the database
            cursor.execute("""
                SELECT COUNT(*)
                FROM Laps2
                WHERE lapDataInfo_sessionId = ? AND laps_lapNr = ? AND laps_timeOfDay = ?
                """, (session_id, lap_nr, time_of_day))
            existing_record_count = cursor.fetchone()[0]

            if existing_record_count > 0:
                #print("Data already exists.")
                continue

            # Extract remaining lap information
            lap_time = lap["lapTime"]
            diff_with_last_lap = lap["diffWithLastLap"]
            diff_with_best_lap = lap["diffWithBestLap"]
            speed = lap["speed"]
            in_pit = lap["inPit"]
            status = lap["status"][0] if lap["status"] else None  # Assuming status is always a list
            field_comparison = lap["fieldComparison"]

            # Extract field comparison information
            position = field_comparison["position"]
            leader_lap = field_comparison["leaderLap"]
            diff_time = field_comparison["diff"]["time"]
            diff_laps = field_comparison["diff"]["laps"]
            gap_ahead_time = field_comparison["gapAhead"]["time"]
            gap_ahead_laps = field_comparison["gapAhead"]["laps"]
            gap_behind_time = field_comparison["gapBehind"]["time"] if field_comparison.get("gapBehind") else None
            gap_behind_laps = field_comparison["gapBehind"]["laps"] if field_comparison.get("gapBehind") else None

            # Prepare SQL INSERT query for lap fields
            insert_query = """
            INSERT INTO Laps2 (
                lapDataInfo_sessionId, lapDataInfo_participantInfo_name, lapDataInfo_participantInfo_class, 
                lapDataInfo_participantInfo_transponder, lapDataInfo_participantInfo_userId, lapDataInfo_participantInfo_startNr, 
                lapDataInfo_participantInfo_startPos, lapDataInfo_participantInfo_fieldFinishPos, lapDataInfo_participantInfo_classFinishPos, 
                lapDataInfo_lapCount, lapDataInfo_allLapsHaveFieldPos, lapDataInfo_firstLapNr, lapDataInfo_lapsDriven, 
                lapDataInfo_classificationType, lapDataInfo_classificationTypeString,
                laps_lapNr, laps_timeOfDay, laps_lapTime, laps_diffWithLastLap, 
                laps_diffWithBestLap, laps_speed, laps_inPit, laps_status, 
                laps_fieldComparison_position, laps_fieldComparison_leaderLap, 
                laps_fieldComparison_diff_time, laps_fieldComparison_diff_laps, 
                laps_fieldComparison_gapAhead_time, laps_fieldComparison_gapAhead_laps, 
                laps_fieldComparison_gapBehind_time, laps_fieldComparison_gapBehind_laps
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # Execute the query to insert lap data into the database
            cursor.execute(insert_query, (
                session_id, lap_data_info["participantInfo"]["name"], lap_data_info["participantInfo"]["class"], 
                lap_data_info["participantInfo"]["transponder"], lap_data_info["participantInfo"]["userId"], 
                lap_data_info["participantInfo"]["startNr"], lap_data_info["participantInfo"]["startPos"], 
                lap_data_info["participantInfo"]["fieldFinishPos"], lap_data_info["participantInfo"]["classFinishPos"], 
                lap_data_info["lapCount"], lap_data_info["allLapsHaveFieldPos"], lap_data_info["firstLapNr"], 
                lap_data_info["lapsDriven"], lap_data_info["classificationType"], lap_data_info["classificationTypeString"],
                lap_nr, time_of_day, lap_time, diff_with_last_lap, diff_with_best_lap,
                speed, in_pit, status, position, leader_lap, diff_time, diff_laps,
                gap_ahead_time, gap_ahead_laps, gap_behind_time, gap_behind_laps
            ))

        # Commit changes to the database
        conn.commit()
        print("JSON data saved to database successfully.")
    except pyodbc.Error as e:
        # Rollback changes if an error occurs
        conn.rollback()
        print("Error saving JSON data to database:", e)


def save_json_data_to_database2(conn, cursor, json_data, count):
    try:
        # Extract lap data info
        lap_data_info = json_data["lapDataInfo"]
        session_id = lap_data_info["sessionId"]

        # Extract the "name" field from the JSON data
        participant_name = lap_data_info['participantInfo']['name']
        participant_startPos = lap_data_info['participantInfo']['startPos']
        
        # Check if there are laps in the JSON data
        if not json_data.get("laps"):
            print(f"No lap for driver {participant_name}")
            '''
            # Insert record with default values for lap fields
            insert_query = """
            INSERT INTO Laps2 (
                lapDataInfo_sessionId, lapDataInfo_participantInfo_name, lapDataInfo_participantInfo_class, 
                lapDataInfo_participantInfo_transponder, lapDataInfo_participantInfo_userId, lapDataInfo_participantInfo_startNr, 
                lapDataInfo_participantInfo_startPos, lapDataInfo_participantInfo_fieldFinishPos, lapDataInfo_participantInfo_classFinishPos, 
                lapDataInfo_lapCount, lapDataInfo_allLapsHaveFieldPos, lapDataInfo_firstLapNr, lapDataInfo_lapsDriven, 
                lapDataInfo_classificationType, lapDataInfo_classificationTypeString,
                laps_lapNr, laps_timeOfDay, laps_lapTime, laps_diffWithLastLap, 
                laps_diffWithBestLap, laps_speed, laps_inPit, laps_status, 
                laps_fieldComparison_position, laps_fieldComparison_leaderLap, 
                laps_fieldComparison_diff_time, laps_fieldComparison_diff_laps, 
                laps_fieldComparison_gapAhead_time, laps_fieldComparison_gapAhead_laps, 
                laps_fieldComparison_gapBehind_time, laps_fieldComparison_gapBehind_laps
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(insert_query, (
                session_id, lap_data_info["participantInfo"]["name"], lap_data_info["participantInfo"]["class"], 
                lap_data_info["participantInfo"]["transponder"], lap_data_info["participantInfo"]["userId"], 
                lap_data_info["participantInfo"]["startNr"], lap_data_info["participantInfo"]["startPos"], 
                lap_data_info["participantInfo"]["fieldFinishPos"], lap_data_info["participantInfo"]["classFinishPos"], 
                lap_data_info["lapCount"], lap_data_info["allLapsHaveFieldPos"], lap_data_info["firstLapNr"], 
                lap_data_info["lapsDriven"], lap_data_info["classificationType"], lap_data_info["classificationTypeString"],
                None, None, None, None, None,
                None, None, None, None, None, None, None,
                None, None, None, None
            ))

            # Commit changes to the database
            conn.commit()
            return
        '''

        # Iterate through each lap in the "laps" list
        for lap in json_data["laps"]:
            # Extract lap information
            lap_nr = lap["lapNr"]
            time_of_day = lap["timeOfDay"]

            # Print the name and starting position
            print("Participant Name:", participant_name)
            print("Starting Position:", participant_startPos)

            # Check if the record already exists in the database
            cursor.execute("""
                SELECT COUNT(*)
                FROM Laps2
                WHERE lapDataInfo_sessionId = ? AND laps_lapNr = ? AND laps_timeOfDay = ?
                """, (session_id, lap_nr, time_of_day))
            existing_record_count = cursor.fetchone()[0]

            if existing_record_count > 0:
                #print("Data already exists.")
                continue

            # Extract remaining lap information
            lap_time = lap["lapTime"]
            diff_with_last_lap = lap["diffWithLastLap"]
            diff_with_best_lap = lap["diffWithBestLap"]
            speed = lap["speed"]
            in_pit = lap["inPit"]
            status = lap["status"][0] if lap["status"] else None  # Assuming status is always a list
            field_comparison = lap["fieldComparison"]

            # Extract field comparison information
            position = field_comparison["position"]
            leader_lap = field_comparison["leaderLap"]
            diff_time = field_comparison["diff"]["time"]
            diff_laps = field_comparison["diff"]["laps"]
            gap_ahead_time = field_comparison["gapAhead"]["time"]
            gap_ahead_laps = field_comparison["gapAhead"]["laps"]
            gap_behind_time = field_comparison["gapBehind"]["time"] if field_comparison.get("gapBehind") else None
            gap_behind_laps = field_comparison["gapBehind"]["laps"] if field_comparison.get("gapBehind") else None

            # Prepare SQL INSERT query for lap fields
            insert_query = """
            INSERT INTO Laps2 (
                lapDataInfo_sessionId, lapDataInfo_participantInfo_name, lapDataInfo_participantInfo_class, 
                lapDataInfo_participantInfo_transponder, lapDataInfo_participantInfo_userId, lapDataInfo_participantInfo_startNr, 
                lapDataInfo_participantInfo_startPos, lapDataInfo_participantInfo_fieldFinishPos, lapDataInfo_participantInfo_classFinishPos, 
                lapDataInfo_lapCount, lapDataInfo_allLapsHaveFieldPos, lapDataInfo_firstLapNr, lapDataInfo_lapsDriven, 
                lapDataInfo_classificationType, lapDataInfo_classificationTypeString,
                laps_lapNr, laps_timeOfDay, laps_lapTime, laps_diffWithLastLap, 
                laps_diffWithBestLap, laps_speed, laps_inPit, laps_status, 
                laps_fieldComparison_position, laps_fieldComparison_leaderLap, 
                laps_fieldComparison_diff_time, laps_fieldComparison_diff_laps, 
                laps_fieldComparison_gapAhead_time, laps_fieldComparison_gapAhead_laps, 
                laps_fieldComparison_gapBehind_time, laps_fieldComparison_gapBehind_laps
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # Execute the query to insert lap data into the database
            cursor.execute(insert_query, (
                session_id, lap_data_info["participantInfo"]["name"], lap_data_info["participantInfo"]["class"], 
                lap_data_info["participantInfo"]["transponder"], lap_data_info["participantInfo"]["userId"], 
                lap_data_info["participantInfo"]["startNr"], lap_data_info["participantInfo"]["startPos"], 
                lap_data_info["participantInfo"]["fieldFinishPos"], lap_data_info["participantInfo"]["classFinishPos"], 
                lap_data_info["lapCount"], lap_data_info["allLapsHaveFieldPos"], lap_data_info["firstLapNr"], 
                lap_data_info["lapsDriven"], lap_data_info["classificationType"], lap_data_info["classificationTypeString"],
                lap_nr, time_of_day, lap_time, diff_with_last_lap, diff_with_best_lap,
                speed, in_pit, status, position, leader_lap, diff_time, diff_laps,
                gap_ahead_time, gap_ahead_laps, gap_behind_time, gap_behind_laps
            ))

        # Commit changes to the database
        conn.commit()
        print("JSON data saved to database successfully. Count! =", count)
    except pyodbc.Error as e:
        # Rollback changes if an error occurs
        conn.rollback()
        print("Error saving JSON data to database:", e)




########################### END SAVE LAPS IN DATABASE ################################################
######################################################################################################
        


######################################################################################################
#############################  CREATE LAPS TABLE IN DATABASE #########################################
def create_table_manually(conn, cursor):
    try:
        # Check if the table already exists
        def table_exists(table_name):
            try:
                cursor.execute(f"SELECT * FROM {table_name}")
                cursor.fetchone()  # Attempt to fetch a row
                return True  # Table exists
            except pyodbc.Error:
                return False  # Table doesn't exist or an error occurred

        if not table_exists('Laps2'):
            # Construct the CREATE TABLE SQL query
            create_table_query = """
            CREATE TABLE Laps2 (
                ID AUTOINCREMENT PRIMARY KEY,
                lapDataInfo_participantInfo_name VARCHAR(255),
                lapDataInfo_participantInfo_class VARCHAR(255),
                lapDataInfo_participantInfo_transponder VARCHAR(255),
                lapDataInfo_participantInfo_userId VARCHAR(255),
                lapDataInfo_participantInfo_startNr VARCHAR(255),
                lapDataInfo_participantInfo_startPos INT,
                lapDataInfo_participantInfo_fieldFinishPos INT,
                lapDataInfo_participantInfo_classFinishPos INT,
                lapDataInfo_lapCount INT,
                lapDataInfo_allLapsHaveFieldPos BIT,
                lapDataInfo_firstLapNr INT,
                lapDataInfo_lapsDriven INT,
                lapDataInfo_classificationType INT,
                lapDataInfo_classificationTypeString VARCHAR(255),
                lapDataInfo_sessionId INT,
                laps_lapNr INT,
                laps_timeOfDay VARCHAR(255),
                laps_lapTime VARCHAR(255),
                laps_diffWithLastLap VARCHAR(255),
                laps_diffWithBestLap VARCHAR(255),
                laps_speed FLOAT,
                laps_inPit BIT,
                laps_status VARCHAR(255),
                laps_fieldComparison_position INT,
                laps_fieldComparison_leaderLap INT,
                laps_fieldComparison_diff_time VARCHAR(255),
                laps_fieldComparison_diff_laps INT,
                laps_fieldComparison_gapAhead_time VARCHAR(255),
                laps_fieldComparison_gapAhead_laps INT,
                laps_fieldComparison_gapBehind_time VARCHAR(255),
                laps_fieldComparison_gapBehind_laps INT
            )
            """

            # Execute the query to create the table
            cursor.execute(create_table_query)

            conn.commit()
            print("Table 'Laps2' created successfully.")
        else:
            print("Table 'Laps2' already exists.")
    except pyodbc.Error as e:
        print("Error creating table:", e)



############################  END CREATE LAPS TABLE IN DATABASE  ####################################
#####################################################################################################
#####################################################################################################
###############################  CONVERT KART NUMBERS  ##############################################
#import pyodbc

# Function to convert letters G, H, M to numbers 1, 2, 3
def convert_kart_number(kart_number):
    letter_to_number = {
        'G': '1',
        'H': '2',
        'M': '3'
    }
    
    # Check if the last character is one of the specified letters
    if kart_number and kart_number[-1] in letter_to_number:
        # Replace the letter with the corresponding number
        kart_number = kart_number[:-1] + letter_to_number[kart_number[-1]]
    
    return kart_number

# Function to check and update kart numbers in the database
def update_kart_numbers(conn, cursor, Session_ID):
    #cursor = conn.cursor()
    
    # Fetch kart numbers from the database for the specific session ID
    query = """
        SELECT ID, lapDataInfo_participantInfo_startNr 
        FROM Laps2 
        WHERE lapDataInfo_sessionId = ?
    """
    cursor.execute(query, (Session_ID,))
    rows = cursor.fetchall()
    
    for row in rows:
        id, kart_number = row
        new_kart_number = convert_kart_number(kart_number)
        
        if new_kart_number != kart_number:
            # Update the kart number in the database
            cursor.execute("""
                UPDATE Laps2
                SET lapDataInfo_participantInfo_startNr = ?
                WHERE ID = ?
            """, (new_kart_number, id))
    
    # Commit the changes
    conn.commit()

# Replace 'your_database.accdb' with the actual path to your Access database
'''conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=path_to_your_database.accdb;'
)
conn = pyodbc.connect(conn_str)



# Update kart numbers
update_kart_numbers(conn, session_id)

# Close the connection
conn.close()
'''
print("Kart numbers updated.")
#sys.exit()


################################   END CONVERT KART NUMBERS  ########################################
#####################################################################################################  
#####################################################################################################
#####################################################################################################
        