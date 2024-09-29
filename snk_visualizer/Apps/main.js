import {  getFile ,snk_log} from './utils.js'//????




var text_tmp = getFile(visualizer_cfg_path);
visualizer_cfg = jsyaml.load(text_tmp);

load_data = visualizer_cfg['load_data'];
base = visualizer_cfg['base'];

var ip_port = `ws://${visualizer_cfg['ip']}:${visualizer_cfg['port']}`;
ws = new WebSocket(ip_port);//backend ip:port

sce_cfg_path = base + "config.yaml";

text_tmp = getFile(sce_cfg_path);
sce_cfg = jsyaml.load(text_tmp);


// ban_list = jsyaml.load(text_tmp);
DEBUG_MODE = visualizer_cfg['DEBUG_MODE'];



// layers
layer_names = Object.keys(sce_cfg['constellations']);
var sat_paths = {};
var isl_paths = {};
NumLayers = layer_names.length;




for (let idx in layer_names) {
  layerIdx2shellNo[idx] = sce_cfg['constellations'][layer_names[idx]]['shellNo'];
  if (sce_cfg['constellations'][layer_names[idx]]['enable']) {
    sat_paths[idx] = base + layer_names[idx] + "_sats" + ".czml";
  }
  if (sce_cfg['constellations'][layer_names[idx]]['ISL']['enable']) {
    isl_paths[idx] = base + layer_names[idx] + "_isls" + ".czml";

  }
 
}




lump_data = jsyaml.load(getFile(base+"lump.json"));
// status data update by  lumpdate info
  for(let i in layer_names){
   if(load_data.includes("sats") ){
    status_data['sats'][layer_names[i]] = new Array(lump_data['constellations'][layer_names[i]]['sats']['id_list'].length).fill(1);
   }
   if(load_data.includes("isls")){
    status_data['isls'][layer_names[i]] = new Array(lump_data['constellations'][layer_names[i]]['isls']['id_list'].length).fill(1);
   }

  }
  














function dataLoad(viewer) {

 
  

  //satllation load

  if (load_data.includes('sats')) {

    snk_log("-> loading sat...");

    for (let i in layer_names) {

      snk_log(sat_paths[i]);

      var sat_promise = Cesium.CzmlDataSource.load(sat_paths[i]);
      viewer.dataSources.add(sat_promise).then(function (ds) {

        layer_sat_collections[i] = ds.entities;

        ds.entities.values.forEach(entity => {

          if (!sat_collection.getById(entity.id)) {
            sat_collection.add(entity);
          }
        });

        // memory init
        layer_sat_arrs[i] =  ds.entities.getById("SATs")._children;



        layer_sensors[i] = {};

      });


    }
  }



  //isl load
  if (load_data.includes('isls')) {
    snk_log("-> loading isl...");
    for (let i in isl_paths) {
      snk_log(isl_paths[i]);
      var isl_promise = Cesium.CzmlDataSource.load(isl_paths[i]);
      viewer.dataSources.add(isl_promise).then(function (ds) {

        layer_isl_entities[i] = ds.entities;
        layer_isls[i] = ds.entities.getById("iISLs")._children.concat(ds.entities.getById("sISLs")._children);
        layer_sISL_templates[i] = ds.entities.getById("sISLs");
        layer_iISL_templates[i] = ds.entities.getById("iISLs");

      });
    }
    snk_log("-> isl load over");
  }










}










if (typeof Cesium !== "undefined") {
  window.startupCalled = true;
  Cesium.Ion.defaultAccessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJiMzkzZWM0MS1iNjg1LTQ1NzMtYTY2Zi04Y2U5OGFlNDU2NzIiLCJpZCI6NzAyMTUsImlhdCI6MTcyMjY3MzAxN30.tOD9SADvG32qNc7GsK9F6w4G2eJO40ZJ3E1m_YMM5S8";
  


  viewer = new Cesium.Viewer("cesiumContainer", {
    imageryProvider:  
    
    new Cesium.TileMapServiceImageryProvider({
      url: Cesium.buildModuleUrl("../Cesium/Assets/Textures/NaturalEarthII"),
    }),


  });


  viewer._cesiumWidget._creditContainer.style.display = "none";

 

  



  dataLoad(viewer);








}