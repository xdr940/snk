import os
from path import Path
import sys
from utils import json2dict,dict2json,YamlHandler
from structures.snet import *
from structures.entity import *
from structures.scenario_templates import *
import random











def wave2intervals(arr,time_steps):
    # 将数组转换为布尔数组，其中非零元素为True
    # bool_arr = arr != 0

    # 计算布尔数组的差分，找出非零元素序列的开始和结束
    # 注意：numpy.diff 会使数组长度减一，所以我们需要对原始布尔数组进行扩展以匹配区间索引
    diff = np.diff(np.concatenate(([0], arr, [0])))

    # 找到从0变到1（开始）和从1变到0（结束）的位置
    starts = np.where(diff == 1)[0]
    ends = np.where(diff == -1)[0]

    # 因为我们扩展了布尔数组，所以需要将索引调整回原始数组的大小
    intervals = [[start, end - 1] for start, end in zip(starts, ends)]

    # 去除可能的空区间（虽然在这个特定情况下不会发生，但作为一种健壮性检查）
    intervals = [interval for interval in intervals if interval[0] < interval[1]]

    intervals = (np.array(intervals).astype(np.int32)) * time_steps
    intervals = [list(item) for item in intervals]

    return intervals
def generate_square_wave(n, num_periods, duty_ratio, phase):
    # 假设整个序列代表的时间长度是1秒（这个假设可以根据需要调整）
    # 计算采样率
    sps = n  # 因为我们假设整个序列是1秒，所以采样率就是点数

    # 计算每个周期的采样点数
    period_samples = sps / num_periods

    # 确保相位在合理范围内
    p = phase % period_samples

    # 计算高电平（1）和低电平（0）的持续时间（以采样点数计）
    high_duration = int(duty_ratio * period_samples)

    # 生成方波
    square_wave = []
    for i in range(n):
        # 计算当前点在周期内的相对位置，考虑相位偏移
        cycle_index = (i + p) % period_samples

        # 判断当前点是在高电平还是低电平
        if cycle_index < high_duration:
            square_wave.append(1)
        else:
            square_wave.append(0)

    return square_wave
def remove_random_items(lst, num_to_remove=None):
    if num_to_remove is None:
        num_to_remove = random.randint(1, len(lst))

    num_to_remove = min(num_to_remove, len(lst))

    for _ in range(num_to_remove):
        index_to_remove = random.randint(0, len(lst) - 1)
        lst.pop(index_to_remove)

    return lst

def ISLs(cfg_path):
    global positions
    yml = YamlHandler(cfg_path)
    config = yml.read_yaml()
    dump_path = Path(config["dump_path"])
    # update cfg file
    os.system("cp {} {}".format(cfg_path, dump_path / "config.yaml"))

    print("\nGENERATES ISLs...")

    random.seed(config['random_seed'])


    '''date time load'''
    sce_start_time = datetime.fromisoformat(config['start_time']).replace(tzinfo=pytz.UTC)
    sce_end_time = datetime.fromisoformat(config['end_time']).replace(tzinfo=pytz.UTC)

    isl_start_time = sce_start_time
    isl_end_time = sce_end_time

    isl_start_stamp = isl_start_time.timestamp()
    isl_end_stamp = isl_end_time.timestamp()
    num_stamps = int(isl_end_stamp - isl_start_stamp)

    # stamps num




    constellations = config['constellations']
    lump_data = json2dict(dump_path /"lump.json")
    snet = sNet()
    '''layer circle'''
    for layer_name,layer in constellations.items():
        if not layer['enable'] or not layer['ISL']['enable']:
            continue

        # layer parameter load
        print("-> ==={}===".format(layer_name))
        num_orbit= layer['num_orbits']
        num_sat = layer['num_sats_per_orbit']
        phase_factor = layer['phase_factor']
        ISL_args = layer['ISL']
        circuit = ISL_args['circuit']
        iISL_conn_features_periods =ISL_args['iISL']['conn_features_periods']
        sISL_conn_features_periods = ISL_args['sISL']['conn_features_periods']



        iISL_rgba = ISL_args['iISL']["rgba"]
        sISL_rgba = ISL_args['sISL']["rgba"]
        iISLs_template["polyline"]["material"]["solidColor"]["color"]["rgba"] = iISL_rgba
        sISLs_template["polyline"]["material"]["solidColor"]["color"]["rgba"] = sISL_rgba
        iISL_duty_ratio = ISL_args['iISL']["duty_ratio"]
        sISL_duty_ratio = ISL_args['sISL']["duty_ratio"]
        iISL_num_periods = ISL_args['iISL']["num_periods"]
        sISL_num_periods = ISL_args['sISL']["num_periods"]

        time_steps = ISL_args['time_steps']
        if num_stamps > 1e4:
            square_wave_stamps = int(num_stamps / time_steps)
        else:
            square_wave_stamps = num_stamps


        #get adjacency by topo
        snet.add_layer(
            layer_name=layer_name,
            sat_id_list= lump_data['constellations'][layer_name]['sats']['id_list'],
            num_orbit=num_orbit,
            num_sat=num_sat,
            phase_factor=phase_factor,
            iISL_conn_features_periods=iISL_conn_features_periods,
            sISL_conn_features_periods=sISL_conn_features_periods,
            circuit=circuit
        )

        snet.build_graph()
        iISL_adj_mat,sISL_adj_mat,adj_mat = snet.get_adj_mat(layer_name=layer_name)


        ISLs_czml_list=[]
        ISLs_czml_list.append(document_template)
        ISLs_czml_list.append(ISLs_template)
        ISLs_czml_list.append(iISLs_template)
        ISLs_czml_list.append(sISLs_template)

        # unreliable isl
        # duty ratio available_stamps
        available_intervals = {}
        for (name_i,name_j) in iISL_adj_mat:# for k,v in
            if iISL_duty_ratio == 1:
                break
            id = "ISL-{}-{}".format(name_i,name_j)

            phase = random.randint(0,square_wave_stamps)%square_wave_stamps
            wave = generate_square_wave(square_wave_stamps, duty_ratio=iISL_duty_ratio, num_periods=iISL_num_periods, phase=phase)
            available_intervals[id] = wave2intervals(np.array(wave),time_steps)


        for (name_i, name_j) in sISL_adj_mat:  # for k,v in
            if sISL_duty_ratio ==1:
                break
            id = "ISL-{}-{}".format(name_i, name_j)
            phase = random.randint(0,square_wave_stamps)%square_wave_stamps
            wave = generate_square_wave(square_wave_stamps, duty_ratio=sISL_duty_ratio, num_periods=sISL_num_periods, phase=phase)
            available_intervals[id] =  wave2intervals(np.array(wave),time_steps)




        '''stage3: construct ISLs CZML file without intervals'''
        ISLs_obj_list=[]
        for (name_i,name_j) in adj_mat:# for k,v in
            name = "ISL-{}-{}".format(name_i,name_j)
            id = "ISL-{}-{}".format(name_i,name_j)
            description = "ISL-{}-{}".format(name_i,name_j)
            ref = ["SAT-{}#position".format(name_i),"SAT-{}#position".format(name_j)] #note!

            isl = ISL(name=name,id=id,description=description,ref=ref)
            if name_i[1:3] != name_j[1:3]:# not in same orbit
                isl.setLineColor(sISL_rgba)
                isl.setParent('sISLs')
            else:
                isl.setLineColor(iISL_rgba)
                isl.setParent('iISLs')


            isl.setTime(isl_start_time,isl_end_time)
            ISLs_czml_list.append(isl.get_item())
            ISLs_obj_list.append(isl)
        ISLs_obj_list = sorted(ISLs_obj_list,key=lambda x:x.id)

        '''stage 4,load intervals'''

        for isl_obj in ISLs_obj_list:
            if isl_obj.parent == 'iISLs' and iISL_duty_ratio <1 :
                this_available_intervals = available_intervals[isl_obj.id]
                isl_obj.intervals_load(this_available_intervals)
            elif isl_obj.parent =='sISLs' and sISL_duty_ratio <1 :
                this_available_intervals = available_intervals[isl_obj.id]
                isl_obj.intervals_load(this_available_intervals)

        ISLs_obj_list = sorted(ISLs_obj_list, key=lambda x: x.id)
        isls_lump = {
            "id_list": [item.id for item in ISLs_obj_list],
            # "data": available_intervals # bug
            "data": None

        }

        ''' stage 5: ISL save '''
        lump_data["constellations"][layer_name].setdefault("isls",isls_lump)
        print("number of ISLs: intral:{}, inter:{}, total:{}".format(len(iISL_adj_mat),len(sISL_adj_mat),len(adj_mat)))

        # data file
        czml_fp = "{}_isls.czml".format(layer_name)
        dict2json(dump_path/czml_fp,ISLs_czml_list)

        # lump file
        dict2json(dump_path/"lump.json",lump_data)

        print("--> CZML: {}/{}".format(dump_path,czml_fp))




if __name__ == "__main__":
    cfg_path = '../configs/2409structure/202f00bm2.yaml'
    if len(sys.argv) > 2:
        print("Usage: python ISLs.py ./config.yaml")
        sys.exit(1)
    elif len(sys.argv) == 2:
        cfg_path = sys.argv[1]
    ISLs(cfg_path)