//------------------  Create key frames -----------------------------------------

function createKeyframe(timeOfDay, layerName, comp, position) {
    var project = app.project.item(1);

    if (project) {
        $.writeln("Project exists");
        var layer = project.layer(layerName);
        if (layer) {
                // Get the index of the nearest keyframe before the specified time
                var prop = layer.property("Transform").property("Position");
                var nearestKeyIndex = prop.nearestKeyIndex(timeOfDay);
                
                // Get the value of the nearest keyframe
                var previousKeyframeValue;
                if (nearestKeyIndex > 0) {
                    previousKeyframeValue = prop.keyValue(nearestKeyIndex);
                } else {
                    // No keyframes before the specified time
                    previousKeyframeValue = prop.valueAtTime(0);
                }

                // Set a keyframe just before the change
                var keyframeTime = timeOfDay - 0.2; // 0.2 seconds before the new position
                $.writeln("previous keyframe Y: " + previousKeyframeValue[1]);
                prop.setValueAtTime(keyframeTime, previousKeyframeValue); // Set keyframe just before the change

                // Create a keyframe at the specified time
                var timeInSeconds = timeOfDay; // Convert time to seconds
                // Calculate X and Y position
                var X = 120;
                var Y = parseInt(position.slice(1)); // Extract Y position from the position string
                Y = (35 * Y) + 115; //default Y = (35 * Y) + 115;
                // Set keyframe and new position
                prop.setValueAtTime(timeInSeconds, [X, Y]);
                $.writeln("new Y: " + Y);
            ;
        } else {
            $.writeln("Layer not found: " + layerName);
        }
    } else {
        $.writeln("No project open.");
    }
}

//------------------  Create first key frames -----------------------------------------
// sets / saves starting grid positions
function firstKeyFrame2(callback) {
    var project = app.project;
    if (!project) {
        $.writeln("No project found.");
        return;
    }

    var comp = project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        $.writeln("No active composition found.");
        return;
    }

    for (var i = 1; i <= comp.numLayers; i++) {
        var layer = comp.layer(i);
        var prop = layer.property("Transform").property("Position");
        var keyframeTime = 0; // Set keyframe at time 0
        var currentPosition = prop.value; // Get current position values
        prop.setValueAtTime(keyframeTime, currentPosition); // Set keyframe at time 0 with current position values
    }

    // Execute the callback function after setting all keyframes
    //callback();
}


//---------------------   test / debug --------------------

function printAssumedPositions(jsonData) {
    for (var lap in jsonData) {
        //$.writeln("Lap Key: " + lap);
        if (jsonData.hasOwnProperty(lap)) {
            //$.writeln("check 3");
            var lapData = jsonData[lap];
            for (var i = 0; i < lapData.length; i++) {
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
                           // $.writeln("do we put a nested function here?");
                            //$.writeln("TimeOfDay: " + timeOfDay);
                            $.writeln(position + ": " + assumedPositions[position]);
                            layerName = assumedPositions[position];
                            //$.writeln("Position: " + position)
                            
                            createKeyframe(timeOfDay, assumedPositions[position], "Name Badge", position);
                        }
                    }
                }
            }
        }
    }
}



