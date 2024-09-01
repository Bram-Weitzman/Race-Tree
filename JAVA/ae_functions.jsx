#include keyFrameFunctions.jsx



//------------------ Import Images ---------------------------------------------->

function importImage(filePath){

    // Import the PSD file into the project
    var importedFile = app.project.importFile(new ImportOptions(File(filePath)));


    // Check if the file was imported successfully
    if (importedFile) {
        // Check if a composition is active
        var comp = app.project.activeItem;
        if (comp && comp instanceof CompItem) {
            // Add the imported file as a layer to the active composition
            var layer = comp.layers.add(importedFile);
            // Set layer properties as needed
        } else {
            alert("No active composition found!.");
        }
    } else {
        alert("Failed to import the file.");
    }
}


//------------------  CREATE POSITION NUMBERS ----------------------------------->

function create_position_numbers(yPosition, i, comp, duration){
    var pos_num = (i < 9 ? "  " : " ") + (i + 1);
    
    // Create a text layer for the driver info
    var textLayer = comp.layers.addText(pos_num);
    textLayer.name = "Pos_Number " + (i + 1);
    
    /*
    if (i % 2 === 0){
        // Set text layer position relative to the shape layer
        textLayer.position.setValue([100, yPosition]); // Set position
    } else {
        // Set text layer position relative to the shape layer
        textLayer.position.setValue([375, yPosition]); // Set position 
    }
    */

    // Set text layer position relative to the shape layer
    textLayer.position.setValue([100, yPosition]); // Set position 
    
    // Set the duration of the text layer
    textLayer.outPoint = comp.duration; // Set outPoint to the duration of the composition

    // Set text properties
    var textProperty = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
    var textDoc = textProperty.value;
    textDoc.fontSize = 36; // Font size
    textDoc.fillColor = [1, 1, 1]; // Text color (black)
    textDoc.font = "Xolonium"; // Font family
    textDoc.applyFill = true; // Enable fill

    // Apply the modified text properties
    textProperty.setValue(textDoc);

    // Alert message
    // alert("Name badge created successfully!");
}

//------------------------------------------------------------------------------------------------------>




//-------------------  Function - Create Name Badge ---------------------------------------------------->
// STILL NEEDS FORMATING OF TEXT.
// WOULD LIKE TO ADD IMAGE OF HELMET
//  THIS MIGHT HELP MAKE THE SIZES EVEN
// FUNCTIONALITY TO "CENTRE" KART NUMBERS

function create_name_badge(yPosition, i, comp) {

    var driverName = startingGrid[i].name;

    // Convert the name to uppercase for comparison
    var driverNameUpper = driverName.toUpperCase();

    // Initialize firstName and lastName variables
    var firstName, lastName;

    // Check for the specific exception
    if (driverNameUpper === "RAUL GABRIEL CANUTO") {
        firstName = "Gabriel";
        lastName = "Canuto";
    } else {
        // Split the name into parts
        var parts = driverName.split(/\s+/);

        // Extract the first name
        firstName = parts[0];

        // Join the remaining parts to form the last name
        lastName = parts.slice(1).join(' ');
    }

    // Get the first letter of the first name
    var firstLetter = firstName.charAt(0);

    // Get the kart number
    var kartNumber = startingGrid[i].kartNumber;


    /*
    var driverName = startingGrid[i].name;
    var lastName = driverName.split(/\s+/)[1];
    var firstThreeLetters = lastName.substring(0, 3);
    var firstName = driverName.split(" ")[0];
    var firstLetter = firstName.charAt(0);
    var kartNumber = startingGrid[i].kartNumber;
    */

    //var driverInfo = (i < 10 ? "  " : " ") + i + " " + firstLetter + "." + firstThreeLetters + "  " + kartNumber;
    //var driverInfo = (firstLetter + "." + firstThreeLetters + "  " + kartNumber);
    //var driverInfo = (firstLetter + "." + firstThreeLetters);
    //var driverInfo = (firstThreeLetters);
    var driverInfo = (firstLetter + "." + lastName);
    //var driverInfo = (lastName);
    $.writeln(driverInfo);

    // Create a text layer for the driver info
    var textLayer = comp.layers.addText(driverInfo);
    textLayer.name = kartNumber;
    /*
    if (i % 2 === 0){
        // Set text layer position relative to the shape layer
        textLayer.position.setValue([200, yPosition]); // Set position
    } else {
        // Set text layer position relative to the shape layer
        textLayer.position.setValue([475, yPosition]); // Set position 
    }
    */

    // Set text layer position relative to the shape layer
    textLayer.position.setValue([200, yPosition]); // Set position


    // Set text properties
    var textProperty = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
    var textDoc = textProperty.value;
    textDoc.fontSize = 40; // Font size
    textDoc.fillColor = [1, 1, 1]; // Text color (black)
    textDoc.font = "Xolonium"; // Font family
    textDoc.applyFill = true; // Enable fill

    // Apply the modified text properties
    textProperty.setValue(textDoc);

    // Alert message
    // alert("Name badge created successfully!");

}
//------------------------------------------------------------------------------------------------------>
