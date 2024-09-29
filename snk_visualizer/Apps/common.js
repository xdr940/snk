var viewer;

var ws;



var visualizer_cfg_path = "../configs/config.yaml"
var base;

var sce_cfg_path;
var sce_cfg;

var load_data;
var visualizer_cfg;

var lump_data;

var status_data={
    "sats":{},
    "isls":{},
}




     

var layer_names;
var tracked_entity;

var DEBUG_MODE;//cfg



var currentLayerIdx = 0;
var NumLayers;







var layer_isl_entities = {};
var layer_isls = {};


var sat_collection = new Cesium.EntityCollection();
var layer_sat_collections = {};
var layer_sat_arrs = {};






var layer_msl_collections={};
var layer_msl_arrs={};


var fwds;
var fwds_entities;//all used fwds


var fwds_cnt = {};
//
var layer_sensors = {};

var inited = 0;
var startTime;

var msg_from_backend;
var msg_to_backend;
var to_backend_do = 'ack';




// utilzation test

//templates
var layer_iISL_templates={};
var layer_sISL_templates={};
var SAT_template;

//=====================
var layerIdx2shellNo={};




