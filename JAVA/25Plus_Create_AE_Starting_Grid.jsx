// Inclusions
#include 25Plus_ae_functions.jsx
#include keyFrameFunctions.jsx
$.writeln("check 1");

/*
// Create a new composition
var compWidth = 3840; // Width of the composition (4K resolution)
var compHeight = 2160; // Height of the composition (4K resolution)
var compDuration = 1500; // Duration of the composition in seconds
var driverInfo = "";
*/


//------------------- load starting grid json data --------------------------------------------//

// Load JSON file
//var jsonFile = File("F:/AE Scripts/GetData/JSON/starting_grid_data.json");
var jsonFile = File("F:/AE Scripts/RaceTree/starting_grid.json");
jsonFile.open("r");
var jsonString = jsonFile.read();
jsonFile.close();

// Parse JSON data
var jsonData = JSON.parse(jsonString);

var startingGrid = jsonData.startingGrid;

// Count the number of drivers
var numDrivers = jsonData.startingGrid.length;

// Log the number of drivers
$.writeln("Number of drivers!!: " + numDrivers);
//--------------------------------------------------------------------------------//

bgColour = [128, 128, 128]; // Medium grey for testing / Layout
//bgColour = [0,0,0]; // Black for production


// Create a new composition
var newComp = app.project.items.addComp("Name Badge", 3840, 2160, 1.0, 1500, 30);

// Check if the composition was created successfully
if (newComp) {
   //alert("New composition created successfully!");
   newComp.openInViewer();
} else {
    alert("Failed to create a new composition.");
}

//Import background images
var topImage = "F:/AE Scripts/GetData/TopBackground.psd" // path to top image
var bottomImage = "F:/AE Scripts/GetData/BottomBackground.psd" // path to bottom image
var joeKarterHRKC = "F:/AE Scripts/GetData/joekarter.psd" // path to bottom image

importImage(topImage);
importImage(bottomImage);
importImage(joeKarterHRKC);


// Starting y-position for the first text layer
var initialYPosition = 450;



//Loop to create position numbers
for (var i = 0; i < numDrivers; i++) {  
    if ( (i+1) % 2 === 0){
        create_position_numbers(initialYPosition + ((i-1) * 35 + 10), i, newComp, 1500);
        $.writeln("i: " + i);
    } else {
        create_position_numbers(initialYPosition + (i * 35), i, newComp, 1500);
    }
   
}

//Loop to create name badges
for (var i = 0; i < numDrivers; i++) {  
    if ( (i+1) % 2 === 0){
        create_name_badge(initialYPosition + ((i-1) * 35 + 10), i, newComp, 1500);
    } else {
        create_name_badge(initialYPosition + (i * 35), i, newComp, 1500);
    }
}








