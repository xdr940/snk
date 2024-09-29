
// import * as Cesium from '../Cesium/Cesium.js'

import "../Cesium/Cesium.js"
import "./CesiumSensors.js";

export function snk_log(msg,debug_mode) {
  if(debug_mode == DEBUG_MODE){
    console.log(msg);
  }
}


export function init_show() {
  snk_log('-> at init show','normal');

  // FPS
  viewer.scene.debugShowFramesPerSecond = true;

  //sat path false
  for (let l in layer_sat_arrs) {
    for (var i = 0; i < layer_sat_arrs[l].length; i++) {
      layer_sat_arrs[l][i].path.show = false;
    }
    //sat labels false
    for (var i = 0; i < layer_sat_arrs[l].length; i++) {
      layer_sat_arrs[l][i].label.show = false;

    }
  }


  
  //sat
  SAT_template = sat_collection.getById("SATs");

 









}


export function sensorInstall(viewer, satellite, steering_angle, radius, color) {
  // the height of cone named as sensor.radius, cause it is the radius of ball

  var directions = [];
  for (var i = 0; i < 36; ++i) {
    var clock = Cesium.Math.toRadians(10.0 * i);// 弧度
    // var rad = (180 - 2 * steering_angle) / 2;
    var steering_angle_rad = Cesium.Math.toRadians(steering_angle); //starlink sats have 40d elevation, thus, (180-2*40)/2 = 50
    directions.push(new Cesium.Spherical(clock, steering_angle_rad));// new Cesium.Spherical(clock, cone, magnitude); 一组曲线三维坐标
  }



  // sensor.modelMatrix = getModelMatrix();
  var sensor = new CesiumSensors.CustomSensorVolume();
  sensor.radius = radius;
  sensor.directions = directions;
  sensor.lateralSurfaceMaterial = Cesium.Material.fromType('Color');// 侧面材料
  sensor.lateralSurfaceMaterial.uniforms.color = color;





  viewer.scene.preRender.addEventListener((scene, time) => { // preRender: 获取在场景更新之后以及场景渲染之前立即引发的事件。事件的订阅者将Scene实例作为第一个参数，将当前时间作为第二个参数。
    let modelMatrix = satellite.computeModelMatrix(time); // 在指定时间计算实体转换的模型矩阵, -> Matrix4
    Cesium.Matrix4.multiply(
      modelMatrix,
      Cesium.Matrix4.fromRotationTranslation(
        Cesium.Matrix3.fromRotationY(Cesium.Math.toRadians(-180))),
      modelMatrix
    )// multiply 计算两个矩阵的乘积;  fromRotationTranslation 从表示旋转的Matrix3和表示平移的Catresian3中计算Matrix4实例
    sensor.modelMatrix = modelMatrix
  });
  
  viewer.scene.primitives.add(sensor);

  return sensor;
}

export function make_sensor() {
  // var sensor = sensorMaker(30);
  var colors = [];

  var steering_angles = []; //30degree
  var heights = []; //unit ?
  var factors = [];

  for (let i in layer_names) {
    colors.push(sce_cfg['constellations'][layer_names[i]]['sensor']['rgba']);
    steering_angles.push(sce_cfg['constellations'][layer_names[i]]['sensor']['steering_angle']);
    heights.push(sce_cfg['constellations'][layer_names[i]]['sensor']['height']);
    factors.push(sce_cfg['constellations'][layer_names[i]]['sensor']['height_factor']);
  }

  for (let l in layer_sat_arrs) {
    for (var i = 0; i < layer_sat_arrs[l].length; i++) {
      var color = new Cesium.Color(colors[l][0], colors[l][1], colors[l][2], colors[l][3]);
      var radius = heights[l] / Math.cos(steering_angles[l] * Math.PI / 180) * (1 + factors[l]);
      var sensor = sensorInstall(viewer, layer_sat_arrs[l][i], steering_angles[l], radius, color);

      layer_sensors[l][layer_sat_arrs[l][i].id] = sensor;
      layer_sensors[l][layer_sat_arrs[l][i].id].show = false;

    }
    
  }


}




export function make_isl() {
  snk_log('-> making isls...','normal');

  for (let l in layer_isl_entities) {

    var isls = layer_isl_entities[l].getById('sISLs')._children;
    for (let i = 0; i < isls.length; i++) {

      var refprop0 = new Cesium.ReferenceProperty(sat_collection, isls[i].polyline.positions._value[0]._targetId, ['position']);
      var refprop1 = new Cesium.ReferenceProperty(sat_collection, isls[i].polyline.positions._value[1]._targetId, ['position']);

      var refproperty_list = [refprop0, refprop1];
      isls[i].polyline.positions = new Cesium.PositionPropertyArray(refproperty_list);


    }

    isls = layer_isl_entities[l].getById('iISLs')._children;
    for (let i = 0; i < isls.length; i++) {

      var refprop0 = new Cesium.ReferenceProperty(sat_collection, isls[i].polyline.positions._value[0]._targetId, ['position']);
      var refprop1 = new Cesium.ReferenceProperty(sat_collection, isls[i].polyline.positions._value[1]._targetId, ['position']);

      var refproperty_list = [refprop0, refprop1];
      isls[i].polyline.positions = new Cesium.PositionPropertyArray(refproperty_list);


    }

  }


  snk_log('-> isls over','normal');


}



export function getByIdFromAll(entity_id) {

  // snk_log('at get from all');
  // snk_log(entity_id);
  var return_entity;

  var element_arr = entity_id.split('-');
  switch (element_arr[0]) { //entity type
    case 'SAT':
      for (let l in layer_sat_collections) {
        return_entity ||= layer_sat_collections[l].getById(entity_id)
      }
      break;
    case 'MS':
      return_entity = ms_collection.getById(entity_id);
      break;
    case 'ISL':
      var potential_entity_id = 'ISL-' + element_arr[2] + '-' + element_arr[1]
      for (let l in layer_isl_entities) {
        return_entity ||= layer_isl_entities[l].getById(entity_id) || layer_isl_entities[l].getById(potential_entity_id);
      }
      break;

    case 'GSL':
      for (let l in layer_gsl_collections) {
        return_entity ||= layer_gsl_collections[l].getById(entity_id);
      }
      break;
    case 'MSL':
      for (let l in layer_msl_collections) {
        return_entity ||= layer_msl_collections[l].getById(entity_id);

      }
      break;

    case 'GS':
      return_entity = gs_collection.getById(entity_id);

      break;

    case 'eISL':// 容错机制

      for (let l in layer_eisl_entities) {
        return_entity ||= layer_eisl_entities[l].getById(entity_id);
        return_entity ||= layer_eisl_entities[l].getById(element_arr[0] + '-' + element_arr[2] + '-' + element_arr[1]);


      }
      break;

    case 'FWD':
      if (!fwds_entities) break;
      return_entity = fwds_entities.getById(entity_id);
      break;
    case 'tFWD':
      if (!fwds_entities) break;
      return_entity = fwds_entities.getById(entity_id);
      break;


  }




  return return_entity;
}

// get data from visualizer to server
export function get_sats(layer_sat_arrs) {
  var sats_status = [];
  for (let i in layer_sat_arrs) {
    for (var j = 0; j < layer_sat_arrs[i].length; j++) {
      sats_status.push(layer_sat_arrs[i][j].id);
    }

  }

  return sats_status;
}


export function get_isls(time){
  for (let l in layer_isls) {
    var orig_status = new Array(lump_data['constellations'][layer_names[l]]['isls']['id_list'].length).fill(1);

    for (let i in layer_isls[l]) {

      if (!isXslConnected(layer_isls[l][i], time)) {
        var sat_idx = lump_data['constellations'][layer_names[l]]['isls']['id_list'].indexOf(layer_isls[l][i].id);
        orig_status[sat_idx] = 0;
      }
      status_data['isls'][layer_names[l]] =orig_status;
    }
  }

  return status_data['isls'];

}






export function getStateType(stateType_str) {

  switch (stateType_str) {
    case "busy":
      return STATE_BUSY;
    case "idle":
      return STATE_IDLE;
    case "data":
      return TYPE_DATA;
    case "ack":
      return TYPE_ACK;
  }

}










export function getFile(file_path) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', file_path, false);
  xhr.overrideMimeType("text/html;charset=utf-8");
  xhr.send(null);
  if (xhr.status == 404) {
    return false;
  }
  return xhr.responseText;


}

export function show_isl(layerIdx,show_mode){
  if(layer_isl_entities[layerIdx]){
    layer_isl_entities[layerIdx].getById("ISLs").show = show_mode;
  }
}
