#This is the main script
Session_ID = "8188741"



#Imports
from myFunctions import *
import myFunctions
import json
import pyodbc
import database


global_Session_ID = Session_ID


################################### OPEN DB CONNECTION ##################################

database.connect_to_database()
 
#########################################################################################


#Variable for the different sections of the website we need to get data from 
my_base_url = "https://eventresults-api.speedhive.com/api/v0.2.3/eventresults/sessions/"

my_classification = "https://eventresults-api.speedhive.com/api/v0.2.3/eventresults/sessions/8188741/classification"
my_session = "https://eventresults-api.speedhive.com/api/v0.2.3/eventresults/sessions/8188741"
my_laps = my_base_url + Session_ID + "/lapdata/"
print(my_laps)


xhr_url = None
#xhr_url = my_classification

######################### Classification Data ######################################
#Let's call the function to load in the race classification data
#count the number of drivers and save in a variable

global_json_data = function_get_data(my_classification)
# Access the JSON data
if global_json_data is not None:
    classification_data = global_json_data
    num_drivers = 0
    # Extract name and code for each user
    name_code_pairs = [(item['name'], item['user']['chip']['code']) for item in global_json_data['rows']]
    
    # Print the name and code pairs
    for name, code in name_code_pairs:
        #print("Name:", name, "| Code:", code)
        num_drivers = num_drivers +1
        #print (num_drivers)
    
else:
    print("No JSON data available.")

print("total number of drivers is: ",num_drivers)

# Let's call the function to insert session data into the database
myFunctions.insert_classification_data(classification_data)

##################### END OF CLASSIFICATION DATA  ############################
    



##########################  SESSION DATA  ####################################

#Let's call the function to load in the race session data
global_json_data = function_get_data(my_session)

# Access the global variable containing JSON data
if global_json_data is not None:
    #session_data = json.dumps(global_json_data)
    session_data = global_json_data
   # print(session_data)

    
else:
    print("No Session JSON data available.")




# Assuming you have loaded session_data from somewhere
# Let's call the function to insert session data into the database
myFunctions.insert_session_data(session_data, num_drivers)

##########################  END OF SESSION DATA  ################################


############################ LAP DATA ###########################################

# Connect to your Access database
conn, cursor = f_connect_DB()


#Lets call a function to check the database to see if data for the session already exists.
Session_booleon = sql_check_laps(Session_ID, conn, cursor)


if Session_booleon:
    print("data already exists")
else:
    # Loop to call function_get_data() and collect JSON data for each driver
    a = 1
    for i in range(num_drivers):
        # Call function_get_data() and append the returned JSON data to the list
        my_laps2 = my_laps + str(a) + "/laps"
        a = a+1
        #print("HERE")
        print(my_laps2)
        driver_data = function_get_data(my_laps2)  # Assuming function_get_data() takes driver_id as an argument


       

        if driver_data:
            driver_name = driver_data['lapDataInfo']['participantInfo']['name']
            #print ("Driver_Name:", driver_name)
            # Extract session ID for the current driver
            session_id = driver_data['lapDataInfo']['sessionId']
             # Function to get the driver ID based on the driver's name
            driver_id = get_driver_id(driver_name)      
            print ("Driver Name Is:", driver_name)
            
            if driver_id:
                laps = driver_data['laps']
                #laptime = driver_data['lapTime']
                if laps:
                    for index, lap in enumerate(laps, start=1):  # Start index from 1
                         # Extract the time portion from the datetime string for each lap
                        time_str = lap['timeOfDay'].replace("T", " ").split(" ")[1]  # Split by space and get the second part (time)
                        #convert each lap time of day to milliseconds
                        my_time = convert_time(time_str)
                        #print ("Milli is:", my_time)
        
                        if index == 1:  # For the first lap
                            laptime = lap['lapTime']

                            #convert the string to milliseconds
                            milliseconds = seconds_to_milliseconds(laptime)
                            startOfRace = my_time - milliseconds
                            # Insert the first lap data into the database
                            first_insert_query = "INSERT INTO laps (SessionID, DriverID, Lap0TOD, Lap1TOD) VALUES (?, ?, ?, ?)"
                            cursor.execute(first_insert_query, (session_id, driver_id, startOfRace, my_time))
                            conn.commit()
                            print("First lap data inserted into the database.")
                            #lets calculate lap 0 (start of race) in milliseconds and insert that into the database

                        else:
                            # For subsequent laps, update the corresponding column
                            column_name = f"Lap{index}TOD"
                            update_query = f"UPDATE laps SET {column_name} = ? WHERE DriverID = ? AND SessionID = ?"
                            cursor.execute(update_query, (my_time, driver_id, session_id))
                            conn.commit()
                            print(f"Lap data (lap {index}) updated.")

                            laptime = lap['lapTime']
                            print ("First Laptime is: ", laptime)
                else:
                    print("No laps data available for this driver.")
            else:
                print(f"Driver '{driver_name}' not found in the database.")
        else:
            print("Driver data is None for some reason.")

    # Close the cursor and database connection
    cursor.close()
    conn.close()




########################### END OF LAP DATA ####################################

