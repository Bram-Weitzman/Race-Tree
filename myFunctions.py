#Script to get json data from speedhive.mylaps.com
import pyodbc
import datetime
import database




#Global variables
global_json_data = None


################################### Calc Lap times ###########################################

def calculate_lap_time(lap_data):
    for driver_id, laps in lap_data.items():
        prev_lap_tod = None
        for lap in laps:
            curr_lap_tod = lap['lap_tod']
            if prev_lap_tod is not None:
                lap_time_ms = curr_lap_tod - prev_lap_tod
                lap['lap_time_ms'] = lap_time_ms
            prev_lap_tod = curr_lap_tod
    return lap_data


################################################################################################

################################### Purple Laps ################################################

def track_fastest_lap(lap_data):
    fastest_lap_time = float('inf')  # Initialize with a very large value
    fastest_lap_driver = None

    # Iterate through lap data to find the fastest lap
    for lap_number, lap_info in lap_data.items():
        for lap in lap_info:
            lap_tod = lap['lap_tod']
            if lap_tod < fastest_lap_time:
                fastest_lap_time = lap_tod
                fastest_lap_driver = lap['driver_name']

    # Mark the fastest lap in the lap data as "purple"
    if fastest_lap_driver is not None:
        for lap_number, lap_info in lap_data.items():
            for lap in lap_info:
                if lap['driver_name'] == fastest_lap_driver and lap['lap_tod'] == fastest_lap_time:
                    lap['color'] = 'purple'

    return lap_data



################################# End Purple Laps #############################################




#################################### Seconds Time Converter #####################################

def seconds_to_milliseconds(seconds):
    #Convert the string to a float
    seconds = float(seconds)
    # Convert seconds to milliseconds
    milliseconds = seconds * 1000
    return milliseconds





#################################################################################################

##################################### Time Converter ############################################

def convert_time(time_str):

    # Split the time string into hours, minutes, seconds, and milliseconds
    hours, minutes, seconds = time_str.split(":")
    #seconds, milliseconds = seconds_ms.split(".")

    # Convert each part to integers or floats
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds)
    #milliseconds = int(milliseconds)

    # Convert hours and minutes to seconds
    hours_seconds = hours * 3600
    minutes_seconds = minutes * 60

    # Calculate total seconds and milliseconds
    total_seconds = hours_seconds + minutes_seconds + seconds
    total_milliseconds = (total_seconds * 1000)

    print(type(total_milliseconds))
    print("Total seconds:", total_seconds)
    #print("Milliseconds;", milliseconds)
    print("Total milliseconds:", total_milliseconds)

    return total_milliseconds

#################################################################################################

########### GET DRIVER_ID #######################################################################
# Function to get the driver ID based on the driver's name
def get_driver_id(driver_name):
    query = "SELECT ID FROM Drivers WHERE driver_name = ?"
    cursor = database.conn.cursor()
    #print("Driver Name: ", driver_name)

    cursor.execute(query, (driver_name,))
    row = cursor.fetchone()
    if row:
        return row[0]  # Return the ID if found
    else:
        return None  # Return None if driver not found

#################################################################################################



############################# CHECK DATABASE FOR EXISTING LAP DATA ###############################

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


############################ END LAP DATA DATABASE CHECK  ########################################  

def function_get_data(xhr_url):

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
        with open('ALL_response_data.json', 'w') as f:
            json.dump(json_data, f, indent=4)

        print("JSON data written to response_data.json")
        return global_json_data
    else:
        print(f"Failed to retrieve JSON data. Status code: {response.status_code}")

#f_class(xhr_url)

#######################################################################################################################################
    

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



def insert_session_data(session_data, num_drivers):
    try:
        conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=F:\AE Scripts\GetData\myDB.accdb;'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        print("Database connection established successfully.")

        sql_insert2 = '''
            INSERT INTO Sessions2 (Session_id, session_name, comment, event_id, type, start_time, group_name, isMerge, participated, announcements, num_drivers)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            '''

        session_id = session_data['id']
        session_name = session_data['name']
        comment = session_data['comment']
        event_id = session_data['eventId']
        type_ = session_data['type']
        start_time = session_data['startTime']
        group_name = session_data['groupName']
        is_merge = session_data['isMerge']
        participated = session_data['participated']
        announcements = session_data['announcements']

        start_time_iso = start_time
        start_time = datetime.datetime.fromisoformat(start_time_iso.replace("T", " ")).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(sql_insert2, (session_id, session_name, comment, event_id, type_, start_time, group_name,is_merge, participated, announcements, num_drivers))
        conn.commit()
        print("Session data inserted into the database successfully.")

    except Exception as e:
        print("Error inserting session data into the database:", e)
        conn.rollback()
    
    finally:
        conn.close()


def insert_classification_data(classification_data):

    # Connect to the database
    conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=F:\AE Scripts\GetData\myDB.accdb;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Iterate over each row in the JSON data
    for row in classification_data['rows']:
        mstuserid = row['user']['mstUserId'] if row['user']['mstUserId'] else None
        name = row['name']
        startnumber = row['startNumber']
        resultclass = row['resultClass']

        # Define the SQL statement to check for duplicates
        sql_check_duplicate = '''
            SELECT COUNT(*) FROM Drivers WHERE driver_name = ? 
        '''

        # Execute the SQL statement to check for duplicates
        cursor.execute(sql_check_duplicate, (name))
        result = cursor.fetchone()
        #print(result)
        
        # If there are no duplicates, insert the data into the Drivers table
        if result[0] == 0:
            # Define the SQL statement to insert data into the Drivers table
            sql_insert = '''
                INSERT INTO Drivers (mstuserid, driver_name, kart_number, class_1)
                VALUES (?, ?, ?, ?)
            '''
        
            try:
                # Execute the SQL statement
                cursor.execute(sql_insert, (mstuserid, name, startnumber, resultclass))
                conn.commit()
                print("Driver data inserted into the database successfully.")
            except Exception as e:
                print("Error inserting driver data into the database:", e)
                #conn.rollback()  # Rollback the transaction in case of an error
        else:
            print(f"Driver with name '{name}' and start number '{startnumber}' already exists in the database. Skipping insertion.")
            
    # Close the database connection
    conn.close()






def save_code_for_later():
            # If there are no duplicates, insert the data into the Drivers table
        if result[0] == 0:
            # Define the SQL statement to insert data into the Drivers table
            sql_insert = '''
                INSERT INTO Drivers (mstuserid, name, startnumber, resultclass)
                VALUES (?, ?, ?, ?)
            '''
        
            try:
                # Execute the SQL statement
                #cursor.execute(sql_insert, (mstuserid, name, startnumber, resultclass))
                #conn.commit()
                print("Driver data inserted into the database successfully.")
            except Exception as e:
                print("Error inserting driver data into the database:", e)
                #conn.rollback()  # Rollback the transaction in case of an error
        else:
            print(f"Driver with name '{name}' and start number '{startnumber}' already exists in the database. Skipping insertion.")