
import {init_show, make_isl, make_sensor,snk_log} from './utils.js'





//============sat layer ===============

var layer_options=[];
for(let i in layer_names){
  var option = {
    text:layer_names[i],
    onselect: function () {
      currentLayerIdx = i;
    }
  }
  layer_options.push(option);
}
Sandcastle.addToolbarMenu(layer_options);



//============
Sandcastle.addToggleButton("SAT", true, function (checked) {
  show_sat(currentLayerIdx,checked);
});
// new ctrl
// document.getElementById("gses2").onclick = function () {
//   console.log("gses2");

// }


Sandcastle.addToggleButton("ISL", true, function (checked) {
  if(layer_isl_entities[currentLayerIdx]){
    layer_isl_entities[currentLayerIdx].getById("ISLs").show = checked;
  }
});


Sandcastle.addToggleButton("iISL", true, function (checked) {
  if(layer_isl_entities[currentLayerIdx]){
  layer_isl_entities[currentLayerIdx].getById("iISLs").show =checked;
  }
});


Sandcastle.addToggleButton("sISL", true, function (checked) {
  if(layer_isl_entities[currentLayerIdx]){
  layer_isl_entities[currentLayerIdx].getById("sISLs").show =checked;
  }
});




document.getElementById("orbit").onclick = function () {
  if (viewer.selectedEntity){
    viewer.selectedEntity.path.show=~viewer.selectedEntity.path.show;
  }
  else if (layer_sat_arrs[currentLayerIdx]){
    for (var i = 0; i < layer_sat_arrs[currentLayerIdx].length; i++) {
      layer_sat_arrs[currentLayerIdx][i].path.show = ~layer_sat_arrs[currentLayerIdx][i].path.show;
    }
  }
  
  


}





// label图层开启关闭
document.getElementById("label").onclick = function () {
  for (var i = 0; i < layer_sat_arrs[currentLayerIdx].length; i++) {
    layer_sat_arrs[currentLayerIdx][i].label.show = ~layer_sat_arrs[currentLayerIdx][i].label.show;
  }

}
document.getElementById("thisLabel").onclick = function () {

  viewer.selectedEntity.label.show = ~viewer.selectedEntity.label.show ;


}
// fwd 图层开启关闭
// document.getElementById("fwd").onclick = function () {
//   fwd_entities.getById("FWDs").show = !fwd_entities.getById("FWDs").show;

// }


// Sensor 图层开启关闭
document.getElementById("sensor").onclick = function () {

  for (let key in  layer_sensors[currentLayerIdx]) {
    layer_sensors[currentLayerIdx][key].show = !  layer_sensors[currentLayerIdx][key].show;
  }



}
document.getElementById("thisSensor").onclick = function () {
  var selected_sat_id = viewer.selectedEntity.id;
  
  if (selected_sat_id){
    for(let l in layer_sensors){
      if (!(selected_sat_id in  layer_sensors[l]))continue;
      layer_sensors[l][selected_sat_id].show = !  layer_sensors[l][selected_sat_id].show;

    }

  }
 



}






// init
document.getElementById("init").onclick = function () {
  
  if (inited==0){
    init_show();
    make_isl();

    // unnecessary
    make_sensor();


    // make_lisl();
    startTime = viewer.clock.currentTime;

    snk_log("init ok");



  }


}


function show_sat(layerIdx,show_mode){
  layer_sat_collections[layerIdx].getById("SATs").show = show_mode;
}

