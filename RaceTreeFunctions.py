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
######################################################################################################    
#############################  NNUMBER OF DRIVERS  ###################################################

def fnum_drivers(global_json_data):

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
    return num_drivers


#############################  END NUMBER OF DRIVERS  ################################################
######################################################################################################    
######################################################################################################    
#############################  GET SESSION DATA  #####################################################
def get_sessionDATA(my_classification):

        
    import json
    import requests

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
    response = requests.get(my_classification, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        #json_data = response.json()
        sessionDATA = response.json()


        # Write the JSON data to a file with each item on a separate line
        with open('ALL_response_data2.json', 'w') as f:
            json.dump(sessionDATA, f, indent=4)

        print("JSON data written to response_data.json")
        return sessionDATA
    else:
        print(f"Failed to retrieve JSON data. Status code: {response.status_code}")



#########################   END SESSION DATA   ########################################################
#######################################################################################################

#######################################################################################################
########################## CREATE STARTING GRID #######################################################

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
#####################  CALCULATE THE TIME OF DAY FOR THE START OF THE RACE ##########################

def calc_start_TOD(rows):
   
    #get the time of day of P1 at the end of the first lap (data source does not have an accurate timestamp of the start of the first lap)
    first_row = rows[0]
    end_of_lap_1_TOD = first_row[17]# Assuming laps_timeOfDay is at index 17
    lap_time = first_row[18]# Assuming laps_lapTime is at index 18
    if ":" in lap_time: 
        lap_time_minutes, lap_time_seconds = lap_time.split(":")
        lap_time_minutes = int(lap_time_minutes)
        lap_time_seconds = float(lap_time_seconds)
        lap_time = lap_time_seconds + (lap_time_minutes * 60)
    else:
        lap_time = first_row[18]# Assuming laps_lapTime is at index 18

        
    end_of_lap_1_TOD = end_of_lap_1_TOD.split('T')[1]
    # Split the time string into hours, minutes, seconds, and milliseconds
    hours, minutes, seconds = end_of_lap_1_TOD.split(":")
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
    #total_milliseconds = (total_seconds * 1000)

    #print(type(total_milliseconds))
    print("Total seconds:", total_seconds)
    #print("Milliseconds;", milliseconds)
    #print("Total milliseconds:", total_milliseconds)
    end_of_lap_1_TOD = total_seconds
    #debug
    print("lap TOD: " + str(end_of_lap_1_TOD))
    print("lap time: " + str(lap_time))
    # start time of race
    start_time = end_of_lap_1_TOD - float(lap_time)
    #print("adjustment time: " + str(adjustment_time))
    
    return start_time
   


####################  END CALC TOD OF START OF RACE  ################################################
#####################################################################################################

#####################################################################################################
#########################   CREATE LAP DATA   #######################################################


def create_lap_data(rows, adjustment_time, grid_order, lap_number):
    lap_key = "Lap{}".format(lap_number)
    first_lap_data = {lap_key: []}
    #print("grid order: " + str(grid_order))
    
    # Extract the list of kart numbers from grid_order['startingGrid']
    grid_list = grid_order['startingGrid']
    kart_numbers = [entry['kartNumber'] for entry in grid_list]

    for row in rows:
        # Accessing elements of each tuple by index
        name = row[1]  # Assuming lapDataInfo_name is at index 1
        start_nr = row[5]  # Assuming lapDataInfo_startNr is at index 5
        curr_pos = row[24]  # Assuming laps_fieldComparison_position is at index 24
        db_time_of_day = row[17] # Assuming laps_timeOfDay is at index 17
        time_of_day = db_time_of_day.split('T')[1]
        time_of_day = convert_time(time_of_day)
        time_of_day = time_of_day - adjustment_time
        time_of_day = round(time_of_day, 3)
        start_pos = row[6]
        
        # Creating a dictionary for each row
        driver_data = {
            "TimeOfDay": time_of_day,
            "position": curr_pos,
            "name": name,
            "kartNumber": start_nr,
            "StartPosition": start_pos
        }
        
        # Add the driver data to the lap data using the dynamic lap key
        first_lap_data[lap_key].append(driver_data)
        
        # Update the grid order dynamically based on the current positions
        kart_positions = {driver["kartNumber"]: driver["position"] for driver in first_lap_data[lap_key]}
        for driver in first_lap_data[lap_key]:
            kart_number = driver["kartNumber"]
            position = kart_positions[kart_number]
            
            # Check if kart_number exists in kart_numbers list before getting the index
            if kart_number in kart_numbers:
                expected_position = kart_numbers.index(kart_number) + 1
                #print("expected_position: " + str(expected_position))
            else:
                expected_position = None  # Handle this case as required
                print("kart number not in kart_numbers")
            
            if expected_position is not None and kart_positions[kart_number] != expected_position:
                # Resort the positions
                new_order = resort_positions(kart_numbers, kart_number, position)
                kart_numbers = new_order
                
                # Recalculate expected_position based on the updated grid order
                expected_position = kart_numbers.index(kart_number) + 1
                
                # Update the assumed positions for the current driver based on the updated grid order
                assumed_positions = {f"P{i+1}": kart_numbers[i] for i in range(len(kart_numbers))}
                
                driver["Assumed_Positions"] = assumed_positions
                #print("Positions Resorted!")

    # Update grid_order to reflect the new kart positions
    updated_grid_order = {'startingGrid': [{'position': i+1, 'name': '', 'kartNumber': kart} for i, kart in enumerate(kart_numbers)]}

    return first_lap_data, updated_grid_order

def convert_time(time_str):
    # Dummy implementation for conversion
    # You need to replace this with actual logic if necessary
    return float(time_str.replace(':', '.'))

def resort_positions(kart_numbers, kart_number, position):
    # Dummy implementation for resorting positions
    # You need to replace this with actual logic if necessary
    if kart_number in kart_numbers:
        kart_numbers.remove(kart_number)
    kart_numbers.insert(position - 1, kart_number)
    return kart_numbers




#########################  END OF CREATE LAP DAT ################################################
#################################################################################################
#################################################################################################

#################################################################################################
#########################  TIME OF DAY CONVERSION  ##############################################
#########################  Seconds Time Converter  ##############################################

def seconds_to_milliseconds(seconds):
    #Convert the string to a float
    seconds = float(seconds)
    # Convert seconds to milliseconds
    milliseconds = seconds * 1000
    return milliseconds

#################################################################################################
##################################### Time Converter ############################################

def convert_time(time_str):
    #debug
    #print("time_str: " + time_str)
    # Split by space and get the second part (time)
    #time_str = time_str.split('T')[1]  
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
    #total_milliseconds = (total_seconds * 1000)

    #print(type(total_milliseconds))
    #print("Total seconds:", total_seconds)
    #print("Milliseconds;", milliseconds)
    #print("Total milliseconds:", total_milliseconds)
    #print(type(total_seconds))

    return total_seconds
    

#########################  END OF TIME OF DAY CONVERSION  #######################################
#################################################################################################
