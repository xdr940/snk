import json
import yaml
import os
def json2dict(file):
    with open(file, 'r') as f:
        dict = json.load(fp=f)
        return dict
def dict2json(file,dict):
    with open(file, 'w') as f:
        json.dump(dict, f)

def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return lines

def readtles(filename):
    lines = readlines(filename)
    length = len(lines)
    assert(length%3==1,"err")


    reformat_lines=[]
    cnt = 1
    while cnt+3<= length:
        satname,line1,line2 = lines[cnt],lines[cnt+1],lines[cnt+2]
        cnt+=3
        reformat_lines.append([satname,line1,line2])

    return reformat_lines

class YamlHandler:
    def __init__(self, file):
        self.file=file
    def read_yaml(self, encoding='utf-8'):
        """读取yaml数据"""
        with open(self.file, encoding=encoding) as f:
            ret = yaml.safe_load(f.read())

            return ret

    def write_yaml(self, data, encoding='utf-8'):
        """向yaml文件写入数据"""
        with open(self.file, encoding=encoding, mode='w') as f:
            return yaml.safe_dump(data, stream=f, sort_keys=False,default_flow_style=False)

    def save_log(self,dst_dir):
        os.system('cp {} {}'.format(self.file, dst_dir))


