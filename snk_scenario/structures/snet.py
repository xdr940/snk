
import networkx as nx
def paser_entId(entityId):
    entType,others = entityId.split('-')
    if entType =='SAT':
        shell_num= int(others[0])
        orbit_num= int(others[1:3])
        phase_num= int(others[3:])
        return entType,shell_num,orbit_num,phase_num
def numId2Id(entity_type,num_id):
    assert entity_type in ['SAT','GS','MS','ISL']
    assert type(num_id) == str
    return entity_type+'-'+num_id

class sNet:
    def __init__(self):
        self.layer_names=[]
        self.cfg={}
        self.positions = None
        self.cnst_adj_table = {}
        self.G_final = None
    def add_layer(self,
            layer_name,sat_id_list,num_orbit,num_sat,
            iISL_conn_features_periods,sISL_conn_features_periods,
            phase_factor,circuit):
        self.layer_names.append(layer_name)
        self.cfg[layer_name]={}
        self.cfg[layer_name].setdefault('sat_id_list',sat_id_list)
        self.cfg[layer_name].setdefault('num_orbit',num_orbit)
        self.cfg[layer_name].setdefault('num_sat',num_sat)
        self.cfg[layer_name].setdefault('iISL_conn_features_periods',iISL_conn_features_periods)
        self.cfg[layer_name].setdefault('sISL_conn_features_periods',sISL_conn_features_periods)
        self.cfg[layer_name].setdefault('phase_factor',phase_factor)
        self.cfg[layer_name].setdefault('circuit',circuit)





    def diff_inter_intral(self,sat1, sat2):
        _,shell_num1,orb_num1,phase_num1 = paser_entId(sat1)
        _,shell_num2,orb_num2,phase_num2 = paser_entId(sat2)
        assert (shell_num1==shell_num2,"functions 'diff_intral_inter' only works in the same shell!")
        num_sat = self.cfg[self.layer_names[shell_num1]]['num_sat']
        num_orbit = self.cfg[self.layer_names[shell_num2]]['num_orbit']
        circuit = self.cfg[self.layer_names[shell_num1]]['circuit']

        if circuit:
            diff_inter =  min((orb_num1 - orb_num2)%num_orbit, (orb_num2 - orb_num1)%num_orbit)
        else:
            diff_inter = max(orb_num1,orb_num2) - min(orb_num1,orb_num2)

        diff_intral =  min((phase_num1 - phase_num2)%num_sat, (phase_num2 - phase_num1)%num_sat)

        return diff_inter,diff_intral


    def __build_adjacent_sats__(self, sat_numId):
        '''
        FOR ISL BUILDING, EVALUATIONS
        motif design
        :param sat_name:
        :return:
        '''
        shell_no = int(sat_numId[0])
        layer_name = self.layer_names[shell_no]

        this_orbit_no = int(sat_numId[1:3])
        this_sat_no = int(sat_numId[3:5])
        intra_itv = len(self.cfg[layer_name]['iISL_conn_features_periods'])
        inter_itv = len(self.cfg[layer_name]['sISL_conn_features_periods'])
        num_orbit = self.cfg[layer_name]['num_orbit']
        num_sat = self.cfg[layer_name]['num_sat']
        circuit = self.cfg[layer_name]['circuit']
        phase_factor = self.cfg[layer_name]['phase_factor']

        adj_sats = []
        iISL_conn_features_periods = self.cfg[layer_name]['iISL_conn_features_periods']
        sISL_conn_features_periods = self.cfg[layer_name]['sISL_conn_features_periods']
        adj_sats_intral = []
        adj_sats_inter = []
        # intral-orbit ISLs
        for idx, connectivity_features in enumerate(iISL_conn_features_periods):
            for delta in connectivity_features:
                if this_sat_no % intra_itv == idx:
                    adj_sats_intral.append(
                        "{:01d}{:02d}{:02d}".format(shell_no, this_orbit_no, (delta + this_sat_no) % num_sat))

        # inter-orbit ISL
        for idx, connectivity_features in enumerate(sISL_conn_features_periods):
            for delta in connectivity_features:
                next_orbit_no = (this_orbit_no + 1) % num_orbit

                if next_orbit_no == 0 and circuit == False:
                    continue

                # if this orbit no == last no, then take phase factor for consideration to make side link
                if next_orbit_no == 0:
                    next_orbit_sat_no = (delta + this_sat_no + phase_factor) % num_sat
                else:
                    next_orbit_sat_no = (delta + this_sat_no) % num_sat

                if this_orbit_no % inter_itv == idx:
                    adj_sats_inter.append("{:01d}{:02d}{:02d}".format(shell_no, next_orbit_no, next_orbit_sat_no))

        return (adj_sats_intral, adj_sats_inter)



    def get_adj_mat(self,layer_name):
        '''
        ISL building
        :return:
        '''
        sat_id_list =  self.cfg[layer_name]['sat_id_list']

        # retun
        iISL_adj_mat = set()
        sISL_adj_mat = set()
        adj_mat = set()
        for sat_id in sat_id_list:
            numId = sat_id.split('-')[1]

            # intral_sats,inter_sats = topo.adjacent_sats_full(numId)
            intral_sats, inter_sats = self.__build_adjacent_sats__(numId)


            for adj_numId in intral_sats:
                if (numId, adj_numId) in iISL_adj_mat or (adj_numId, numId) in iISL_adj_mat:
                    continue
                iISL_adj_mat.add((numId, adj_numId))

            for adj_numId in inter_sats:
                if (numId, adj_numId) in sISL_adj_mat or (adj_numId, numId) in sISL_adj_mat:
                    continue
                sISL_adj_mat.add((numId, adj_numId))

            adj_mat = iISL_adj_mat | sISL_adj_mat

        return iISL_adj_mat,sISL_adj_mat,adj_mat

    def getISLs(self):
        isl_id_list =[]
        for layer_name in self.layer_names:
            adj_sat_intral,adj_sats_inter,adj_mat = self.get_adj_mat(layer_name)
            for sati,satj in adj_mat:
                isl_id_list.append(
                    "ISL-{}-{}".format(sati,satj)
                )

        return isl_id_list

    def build_graph(self):
        # adj table init
        ISLs = self.getISLs()
        for isl in ISLs:
            _, sati_numId, satj_numId = isl.split('-')
            satiId, satjId = numId2Id('SAT', sati_numId), numId2Id('SAT', satj_numId)
            if satiId == satjId:
                print("-> ISLs error!")
                exit(1)
            self.cnst_adj_table.setdefault(satiId, [])
            self.cnst_adj_table.setdefault(satjId, [])

            self.cnst_adj_table[satiId].append(satjId)
            self.cnst_adj_table[satjId].append(satiId)

        self.cnst_G = nx.Graph()
        for sat1 in self.cnst_adj_table.keys():
            for sat2 in self.cnst_adj_table[sat1]:
                self.cnst_G.add_edge(sat1, sat2)


        self.G_final = self.cnst_G.copy()






