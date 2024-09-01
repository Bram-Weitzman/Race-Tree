//------------------  Create Lap Counter Layers  -------------------------------->


function create_lap_counter_layers(compName, lapNumber, callback) {
    var comp = selectProject(compName);
     
    // Check if the layer already exists
    var existingLayer = null;
    for (var i = 1; i <= comp.layers.length; i++) {
        
        var curLayer = comp.layers[i];
        if (curLayer && curLayer.name === "Lap " + lapNumber) {
           
            existingLayer = curLayer;

            // Set opacity to 0
            var opacityProp = curLayer.property("Transform").property("Opacity");
            opacityProp.setValueAtTime(0, 0);

            // Set keyframe for opacity at time 0
            opacityProp.setValueAtTime(0, 0);
            break;
        }
        if (lapNumber == 1) {
            existingLayer = curLayer;
            //$.writeln("lapnumber: " + lapNumber);
            // Set opacity to 100
            var opacityProp = curLayer.property("Transform").property("Opacity");
            opacityProp.setValueAtTime(100, 0);

            // Set keyframe for opacity at time 0
            opacityProp.setValueAtTime(0, 0);
            break;
        }
    }

    // If the layer doesn't exist, create it
    if (!existingLayer) {
        $.writeln(" checking if layer exists");
        // Create a text layer for the lap number
        var textLayer = comp.layers.addText("LAP   " + lapNumber);
        textLayer.name = "Lap " + lapNumber;
        
        // Set text layer position relative to the shape layer
        textLayer.position.setValue([200, 315]); // Set position
        
        // Set the duration of the text layer
        textLayer.outPoint = comp.duration; // Set outPoint to the duration of the composition

        // Set text properties
        var textProperty = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
        var textDoc = textProperty.value;
        textDoc.fontSize = 60; // Font size
        textDoc.fillColor = [1, 1, 1]; // Text color (black)
        textDoc.font = "Xolonium"; // Font family
        textDoc.applyFill = true; // Enable fill

        // Apply the modified text properties
        textProperty.setValue(textDoc);

        // Set opacity to 0
        textLayer.opacity.setValue(0);

        // Set keyframe for opacity at time 0
        textLayer.opacity.setValueAtTime(0, 0);

        // Call the callback function if provided
        if (typeof callback === 'function') {
            // Pass the textLayer as an argument to the callback
            callback(textLayer);
        }
    } else {
        // Layer already exists, no need to create
        $.writeln("Lap Number Layer Already Exists!");
        // Call the callback function if provided
        if (typeof callback === 'function') {
            // Pass the existingLayer as an argument to the callback
            callback(existingLayer);
        }
    }
}



//-------------------------  Lap Counter Function ---------------------------------------

function createLapKeyFrames(timeOfDay, lap, comp, callback) {
    // Access the active composition
    var activeComp = app.project.activeItem;
    if (activeComp && activeComp instanceof CompItem) {

        // Split & re-write "LapX" to "Lap X"
        var parts = lap.match(/([a-zA-Z]+)([0-9]+)/); // Split the string into alphabetic and numeric parts
        //var layerName = parts[1] + " " + parts[2]; // Concatenate the parts with a space in between
        var previousLayerName = parts[1] + " " + parts[2]; // Concatenate the parts with a space in between
        var layerName2 = parseInt(parts[2]) + 1;
        var layerName = parts[1] + " " + layerName2.toString();

        //$.writeln("TOD: " + timeOfDay + "  Curr lap  " + layerName);
        //$.writeln("TOD: " + timeOfDay + "  prev lap  " + previousLayerName);

        // Find the layer in the composition
        var layer = activeComp.layer(layerName);
        var layer2 = activeComp.layer(previousLayerName);

        if (layer && layer2) {
            // Create a keyframe at the specified time
            var timeInSeconds = timeOfDay; // Convert time to seconds
            var prop = layer.property("Transform").property("Opacity");
            var prop2 = layer2.property("Transform").property("Opacity");

            // Set Pre-Keyframe just before
            prop.setValueAtTime(timeInSeconds - 0.2, [0]);       
            // Set keyframe and new position
            prop.setValueAtTime(timeInSeconds, [100]);

             // Set Pre-Keyframe just before on previous lap
            prop2.setValueAtTime(timeInSeconds - 0.2, [100]);       
            // Set keyframe and new position
            prop2.setValueAtTime(timeInSeconds, [0]);

            // Call the callback function to indicate completion
            if (typeof callback === "function") {
                callback();
            }
        } else {
            $.writeln("One of the layers doesn't exist.");
        }
    } else {
        $.writeln("Active composition not found or is not a CompItem.");
    }
}



//------------------------- Call Back Function ------------------------------------------

// Define your callback function
function callback() {
    $.writeln("Position keyframes created successfully.");
}

//------------------------ Load JSON File Data -----------------------------------------

function loadFile(lapNum, Callback){
    var lapFile = new File("F:/AE Scripts/GetData/Laps/Lap_" + lapNum + ".json");
    lapFile.open("r");
    var lapData = lapFile.read();

    lapFile.close();    
    var jsonData = JSON.parse(lapData);

        // Call the callback function to indicate completion
    if (typeof callback === "function") {
        callback();
    }
    return jsonData;
}


//------------------------  Create PreKeyFrame  -----------------------------------------
//  Create a keyframe 10 frames before change to keep the layer from moving early
function preKeyFrame(timeOfDay, layerName, comp, position, callback) {
    // Access the active composition
    var activeComp = app.project.activeItem;
    //$.writeln("layerName: " + layerName);
    if (/^[0-9]+$/.test(layerName)) {
        if (activeComp && activeComp instanceof CompItem) {
            // Find the layer in the composition
            var layer = activeComp.layer(layerName);

            if (layer) {
                // Get the property
                var prop = layer.property("Transform").property("Position");
                
                // Get the index of the nearest keyframe before the specified time
                var nearestKeyIndex = prop.nearestKeyIndex(timeOfDay - 0.001); // Subtract a very small value
                
                // Print the time of the nearest keyframe
                if (nearestKeyIndex >= 1) {
                    var nearestKeyTime = prop.keyTime(nearestKeyIndex);
                    //$.writeln("Time of Nearest Keyframe: " + nearestKeyTime);
                }
                
                // Get the value of the nearest keyframe
                var previousKeyframeValue;
                if (nearestKeyIndex >= 1) { // Check if keyframe index exists
                    previousKeyframeValue = prop.keyValue(nearestKeyIndex);
                } else {
                    // No keyframes before the specified time, use the initial value
                    previousKeyframeValue = prop.valueAtTime(0);
                }

                // Set a keyframe just before the change
                //--------------------------------------------------------------------------------------------------------------------
                // needs to be really small for now otherwise there is the possibility of the prekey overlaping with a previous key.
                var keyframeTime = timeOfDay - 0.2; // Subtract a very small value
                //if the time of the prekey is within 1 second of the previous key, and the value is the same, don't add a pre key
                //need to know: 
                //---the value of the previous key
                //previousKeyframeValue
                //---the time of the previous key
                //nearestKeyTime
                //---the value of this prekey
                //time of this prekey
                //////
                //if (keyframeTime - nearestKeyTime < 3){
                //    $.writeln("PreKey Not Set")
                //    }else{//else, add the prekey
                    prop.setValueAtTime(keyframeTime, previousKeyframeValue); // Set keyframe just before the change
                    //$.writeln("Time of New PreKeyframe: " + keyframeTime);
                //}
                


            }
        }
    }else{
        $.write("layerName has letters")
    }
    // Call the callback function to indicate completion
    if (typeof callback === "function") {
        callback();
    }
}


//------------------------  Create KeyFrames --------------------------------------------

function createKeyframe(timeOfDay, layerName, comp, position, callback) {
    // Access the active composition
    var activeComp = app.project.activeItem;
    //$.writeln("layerName: " + layerName);
    if (/^[0-9]+$/.test(layerName)) {
        if (activeComp && activeComp instanceof CompItem) {
            // Find the layer in the composition
            var layer = activeComp.layer(layerName);
            //var layer = project.layer(layerName);
            //$.writeln("TimeOfDay: " + timeOfDay);
            // Create a keyframe at the specified time
            var timeInSeconds = timeOfDay; // Convert time to seconds
            // Calculate X and Y position
            var X = 200;
            var Y = parseInt(position.slice(1)); // Extract Y position from the position string
            Y = (70 * Y) + 355;//default Y = (70 * Y) + 355;
            var prop = layer.property("Transform").property("Position");



            // Set keyframe and new position
            prop.setValueAtTime(timeInSeconds, [X, Y]);
            //$.writeln("new Y: " + Y);
            // Call the callback function to indicate completion
            if (typeof callback === "function") {
                callback();
                }
            }else{
            $.writeln("ooops")
            }
    }else{
        $.writeln("LayerName Has Letters2")
    }
}

//------------------------  Load json data ----------------------------------------------
function loadJSON(jsonData, callback) {
    var loopCount = 1;
    for (var lap in jsonData) {
        //$.writeln("Lap Key: " + lap);
        if (jsonData.hasOwnProperty(lap)) {
            //$.writeln("check 3");
            var lapData = jsonData[lap];
            for (var i = 0; i < lapData.length; i++) {
                //$.writeln("LoopCount " + loopCount)
                loopCount++;
                //$.writeln("check 5");
                var driver = lapData[i];
                if (driver.hasOwnProperty("Assumed_Positions")) {
                    //$.writeln("check 6");
                    var timeOfDay = driver.TimeOfDay;
                    var assumedPositions = driver.Assumed_Positions;
                    //$.writeln("TimeOfDay: " + timeOfDay);
                    for (var position in assumedPositions) {
                        //$.writeln("check 7");
                        
                        if (assumedPositions.hasOwnProperty(position)) {
                           
                            //$.writeln("TimeOfDay: " + timeOfDay);
                            $.writeln("Posistion: " + position + ": " + assumedPositions[position]);
                            layerName = assumedPositions[position];
                            
                            preKeyFrame(timeOfDay, assumedPositions[position], "Name Badge", position, callback);
                            createKeyframe(timeOfDay, assumedPositions[position], "Name Badge", position, callback);
                            //createLapKeyFrames(timeOfDay, lap, "Name Badge", callback);
                            //$.writeln("do we put a nested function here?");
                        }
                    }
                }
            }
        }
    }
}
//------------------------  Load json data 2 ----------------------------------------------

function loadJSON2(jsonData, callback) {
    var lapNumber;
    var firstTimeOfDay;

    for (var lap in jsonData) {
        if (jsonData.hasOwnProperty(lap)) {
            lapNumber = lap;
            firstTimeOfDay = jsonData[lap][0].TimeOfDay;
            //$.writeln("here i am")
            break;
        }
    }

    if (lapNumber && firstTimeOfDay) {
        createLapKeyFrames(firstTimeOfDay, lapNumber, "Name Badge", callback);
        //$.writeln("LapNumber " + lapNumber + " TOD " + firstTimeOfDay);
    } else {
        // Handle the case where lapNumber or firstTimeOfDay is not found
        // This could happen if the jsonData object is empty or malformed
    }
}



//-------------------------  Select Project & Composition --------------------------------
function selectProject(compName) {
    var project = app.project;
    if (!project) {
        $.writeln("No project found.");
        return null; // Return null if no project is found
    }

    // Loop through the compositions in the project
    //$.writeln("CompName: " + compName);
    for (var i = 1; i <= project.numItems; i++) {
        var item = project.item(i);
        if (item && item instanceof CompItem && item.name === compName) {
            // Return the composition if its name matches
            return item;
        }
    }

    // If no composition with the specified name is found, log and return null
    $.writeln("Composition '" + compName + "' not found.");
    return null;
}


//--------------------------  Clear existing Key Frames --------------------
function clearKeyframes(compName) {
    var comp = selectProject(compName);
    if (!comp) {
        $.writeln("Composition not found or is null.");
        return;
    }

    // Loop through all layers in the composition
    for (var i = 1; i <= comp.numLayers; i++) {
        var layer = comp.layer(i);
        // Check if the layer has the Transform property group
        if (layer.transform) {
            // Loop through properties under the Transform group
            var transformGroup = layer.transform;
            for (var j = 1; j <= transformGroup.numProperties; j++) {
                var prop = transformGroup.property(j);
                // Check if the property has any keyframes
                if (prop.numKeys > 0) {
                    // Remove all keyframes from the property
                    for (var k = prop.numKeys; k >= 1; k--) {
                        prop.removeKey(k);
                    }
                }
            }
        }
    }
    //alert("KeyFrames Cleared!")
        // Call the callback function to indicate completion
    if (typeof callback === "function") {
        callback();
    }
}



//------------------  Create first key frames -----------------------------------------
function createFirstKeyframes(compName, callback) {
    var comp = selectProject(compName);
    if (!comp) {
        $.writeln("Composition not found or is null.");
        return;
    }

        // Loop through all layers in the composition
        for (var i = 1; i <= comp.numLayers; i++) {
            var layer = comp.layer(i);
            //$.writeln("layerName: " + layer.name);
            if (/^[0-9]+$/.test(layer.name)) {
                // Check if the layer has the Transform property group
                //$.writeln("whaaaaaat");
                if (layer.transform) {
                    // Access the position property under the Transform group
                    var positionProp = layer.transform.position;
                    // Set a keyframe at time 0 with the current position
                    positionProp.setValueAtTime(0, positionProp.value);
                }
            }else{
                //$.writeln("LayerNameHasLetters" + layer.name);
            }
        }
    // Call the callback function if provided
    if (typeof callback === 'function') {
        callback();
    }
}