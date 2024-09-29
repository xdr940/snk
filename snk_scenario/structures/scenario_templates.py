root={
    "id":"root",
    "name":"root",
    "parent":None
}
document_template ={
        "id": "document",
        "version": "1.0"
    }

ISLs_template = {
        "id":"ISLs",
        "name":"ISLs",
        "description":"collection of ISL",
        "parent":"root"
      }

sISLs_template = {
    "id": "sISLs",
    "name": "sISLs",
    "description": "collection of sISLs",
    "parent": "ISLs",
    "polyline": {
        "width": 2,
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [
                        0,
                        255,
                        0,
                        150
                    ]
                }
            }
        },

    }

}
iISLs_template={
    "parent": "ISLs",
    "id": "iISLs",
    "name": "iISLs",
    "description": "collection of iISLs",
    "polyline":{
        "width": 2,
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [
                        0,
                        255,
                        0,
                        150
                    ]
                }
            }
        },

    }
}


Sats_template = {
        "id":"Sats",
        "name":"Sats",
        "description":"collection of MS Sats",
        "parent": "MSes",
        "model": {
            "gltf":"/Libs/3d_models/camSat.glb",
            "scale": 0.5,
            "minimumPixelSize": 64,
            "runAnimations": False,
            "show":False
        }
}

