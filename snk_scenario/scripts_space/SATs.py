
# ========public lib=====
import os
import sys
import argparse
from datetime import datetime
from path import Path
import json

# ========custom lib=====
from satgen import generate_tles_from_scratch_with_sgp
from satgen import generate_tles_from_scratch_manual
from satgen import generate_tles_from_tle_seed
from satellite_czml import SatelliteCzml


from utils import YamlHandler
from utils import json2dict,dict2json,readtles


root={
    "id":"root",
    "name":"root",
    "parent":None
}
SATs_template = {
        "id":"SATs",
        "name":"SATs",
        "description":"collection of SAT",
        "parent": "root",
        "model": {
            "gltf":"/Libs/3d_models/camSat.glb",
            "scale": 0.1,
            "minimumPixelSize": 64,
            "runAnimations": False,
            "show":False
        }


}



def SATs(cfg_path: dict) -> None:
    yml = YamlHandler(cfg_path)
    config = yml.read_yaml()
    dump_path = Path(config["dump_path"])
    # dump_path.mkdir_p()


    print("\nGENERATING CONSTELLATION...")
    print("-> sce duration:{} -> {}".format(config['start_time'],config['end_time']))
    print("-> time step: {} s".format(config['time_step']))

    constellations = config['constellations']

    for layer_name,layer in constellations.items():
        if not layer['enable']:
            continue

        print("-> ==={}===".format(layer_name))
        tle_file_path = dump_path/(layer_name+"_tle.txt")

    # phase_factor = constellation['phase_factor']
    # perigee_degree = constellation['perigee_degree']
    # orbit_shift= phase_factor*360/constellation['num_orbits']/constellation['num_sats_per_orbit']
        if'seed_satellite' in layer.keys() and  layer['seed_satellite']:
            generate_tles_from_scratch_manual(
                filename_out=tle_file_path,
                constellation_name=layer_name,
                shellNo=layer['shellNo'],
                num_orbits=layer['num_orbits'],
                num_sats_per_orbit=layer['num_sats_per_orbit'],
                phase_factor=layer['phase_factor'],
                raan_increment =layer['raan_increment'],
                seed_satellite=layer['seed_satellite']
            )
        elif 'sgp' in layer.keys() and layer['sgp']:

            generate_tles_from_scratch_with_sgp(
                filename_out=tle_file_path,
                constellation_name=layer_name,

                num_orbits=layer['num_orbits'],
                num_sats_per_orbit=layer['num_sats_per_orbit'],

                phase_diff=layer['sgp']['phase_diff'],
                inclination_degree =  layer['sgp']['inclination_degree'],
                eccentricity = layer['sgp']['eccentricity'],
                arg_of_perigee_degree = layer['sgp']['perigee_degree'],
                mean_motion_rev_per_day = layer['sgp']['mean_motion_rev_per_day']
            )
        elif 'seed_tle' in layer.keys() and layer['seed_tle']:
            generate_tles_from_tle_seed(
                filename_out=tle_file_path,
                constellation_name=layer_name,
                shellNo=layer['shellNo'],
                num_orbits=layer['num_orbits'],
                num_sats_per_orbit=layer['num_sats_per_orbit'],
                phase_factor=layer['phase_factor']
            )


        # load tles file
        lines = readtles(tle_file_path)
        container = SatelliteCzml(
            tle_list=lines,
            start_time= datetime.fromisoformat(config['start_time']),
            end_time=datetime.fromisoformat(config['end_time']),
            orb_num=layer['num_orbits'],
            sat_num=layer['num_sats_per_orbit'],
            time_step=config['time_step']
        )






        SATs_czml_list =json.loads(container.get_czml())

        id_list =[]
        for item in SATs_czml_list:
            if item["id"]!="document":
                item["parent"] = SATs_template["id"]

                if 'sat_model' in layer.keys():
                    item.setdefault('model',SATs_template['model'])
                    item['model']['gltf'] = layer['sat_model']['gltf']


                id_list.append(item['id'])
            else:
                item["parent"] = None
        SATs_czml_list.insert(1,root)
        SATs_czml_list.insert(2,SATs_template)

        id_list.sort()

        sat_lump = {
            "id_list": id_list,
            "data": []
        }

        ''' stage5 save '''
        lump_data = json2dict(dump_path/"lump.json")
        lump_data['constellations'][layer_name].setdefault("sats",sat_lump)
        print("--> constellation args:\n \t number of orbit:{}, sat_per_orb:{},phase factor:{}".format(
            layer['num_orbits'],
            layer['num_sats_per_orbit'],
            layer['phase_factor']))

        czml_fp = dump_path/"{}_sats.czml".format(layer_name)
        dict2json(czml_fp,SATs_czml_list)

        dict2json(dump_path/"lump.json",lump_data)



        print("--> CZML: {}/{}".format(dump_path,czml_fp))




if __name__ == "__main__":

    cfg_path = '../configs/mplf2/config.yaml'
    if len(sys.argv) >2:
        print("Usage: python SATs.py ./config.yaml")
        sys.exit(1)
    elif len(sys.argv)==2:
        cfg_path = sys.argv[1]

    SATs(cfg_path=cfg_path)