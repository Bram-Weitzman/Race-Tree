#include AE_KeyFrame_Functions2.jsx

//----------------------  Load json data for lap number  ---------------------------
for (var i = 1; i <= nLaps; i++){
    //if (i == 1){
        //loadJSON(jsonData, myCallbackFunction);
    //} else {
        lapNum = i;
        //$.writeln("i in load json is " + i);
        jsonData = loadFile(lapNum, callback);
        
        loadJSON2(jsonData, callback);
        callback();
    //}
}