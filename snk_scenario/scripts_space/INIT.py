


import sys,os
from path import Path
from utils import YamlHandler,dict2json



def INIT(cfg_path):# INIT
    yml = YamlHandler(cfg_path)
    config = yml.read_yaml()
    dump_path = Path(config["dump_path"])
    dump_path.mkdir_p()
    if dump_path.exists():
        for file in dump_path.files():
            file.remove()


    else:
        dump_path.mkdir_p()

    os.system("cp {} {}".format(cfg_path, dump_path / "config.yaml"))


    lump_fp = dump_path/"lump.json"
    lump_data = {
        "constellations":{

        },
        "gses": {},
        "mses":{}
    }
    for layer_name in config["constellations"].keys():
        lump_data['constellations'].setdefault(layer_name,{})
    dict2json(lump_fp,lump_data)

    print("INITIALIZING.....")

    print("-> {}".format(dump_path))

if __name__ == "__main__":
    cfg_path = '../configs/mplf2/config.yaml'
    if len(sys.argv) > 2:
        print("Usage: python INIT.py ./config.yaml")
        sys.exit(1)
    elif len(sys.argv) == 2:
        cfg_path = sys.argv[1]


    INIT(cfg_path=cfg_path)