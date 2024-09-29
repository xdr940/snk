from datetime import datetime
import numpy as np
import pymap3d as pm

from .scenario_templates import *
import pytz

class BasicEntity():
    def __init__(self):
        self.template={}

    def __getattr__(self, item):
        if item in self.template.keys():
            return self.template[item]


    def get_item(self):
        return self.template

    def setTime(self, start_time, end_time):
        interval = start_time.isoformat() + "/" + end_time.isoformat()

        self.template["availability"] = [interval]
        self.template["polyline"]["show"][0]["interval"] = interval
        self.start_time = start_time
        self.start_stamp = start_time.timestamp()

        self.end_time = end_time
        self.end_stamp = end_time.timestamp()

    def setLabel(self,text):
        self.template['label']['text'] = text
    def setParent(self,parent):
        self.template["parent"] = parent
class xSL(BasicEntity):
    def __init__(self):
        super().__init__()

    def setLineColor(self,rgba=None):
        if not rgba:

            self.template["polyline"]["material"]["solidColor"]["color"]["rgba"] = [0,255,0,150]

        else:
            # self.template["polyline"]["material"]["polylineGlow"]["color"]["rgba"] = [255,0,0,255]

            self.template["polyline"]["material"]["solidColor"]["color"]["rgba"] = rgba
            # self.template["polyline"]["material"]["solidColor"] = {}
            # self.template["polyline"]["material"]["solidColor"]["color"] = {}
            # self.template["polyline"]["material"]["solidColor"]["color"]["rgba"] = rgba
            # self.template["polyline"]["width"] = 1

            # self.template["polyline"]["material"]["polylineGlow"]["color"]["rgba"] = rgba

    def add_interval(self, str, tf=True):
        self.template['polyline']['show'].append(
            {
                "interval": str,
                "boolean": tf
            }
        )




    def intervals_load(self,stamp_intervals):


        pre_time_stamp = self.start_stamp
        intervals_update = []
        self.template["polyline"]["show"] = intervals_update
        ret_intervals=[]
        for start, end in stamp_intervals:
            pre_time = datetime.fromtimestamp(pre_time_stamp, tz=pytz.UTC)

            duration_start_time = datetime.fromtimestamp(self.start_stamp + start, tz=pytz.UTC)
            duration_end_time = datetime.fromtimestamp(self.start_stamp + end, tz=pytz.UTC)



            if duration_end_time.timestamp() > self.end_stamp:
                this_inteval = "{}/{}".format(pre_time.isoformat(), duration_start_time.isoformat())
                intervals_update.append(
                    {
                        "interval": this_inteval,
                        "boolean": False
                    }
                )
                break
            this_inteval = "{}/{}".format(pre_time.isoformat(), duration_start_time.isoformat())

            intervals_update.append(
                {
                    "interval": this_inteval,
                    "boolean":False
                }
            )

            this_inteval = "{}/{}".format(duration_start_time.isoformat(), duration_end_time.isoformat())
            intervals_update.append(
                {
                    "interval": this_inteval,
                    "boolean": True
                }
            )
            ret_intervals.append([start,end])
            pre_time_stamp = duration_end_time.timestamp()
        return ret_intervals
    def get_num_intervals(self):
        return len( self.template['polyline']['show'])
class ISL(xSL):
    def __init__(self,id,name,description,ref):
        super().__init__()

        self.template = {
        "id":"none",
        "name":"none",
        "parent":"iISLs",
        "availability":None,
        "description":None,
        "polyline":{
          "show":[

            {
              "interval":None,
              "boolean":True
            }

          ],
          "width":2,
          "material":{
              # "polylineGlow": {
              #     " glowPower": 0.2,
              #     "taperPower": 1,
              #     "color": {
              #         "rgba": [
              #             0,
              #             255,
              #             255,
              #             255
              #         ]
              #     }
              # },
              "solidColor":{
                  "color":{
                      "rgba": [
                          0,
                          0,
                          255,
                          150
                      ]
                  }
              }
          },
          "arcType":"NONE",
          "positions":{
            "references":[
              "none","none"
            ]
          }
        }
      }

        self.template["id"] = id
        self.template["name"] = name
        self.template["description"] = description
        self.template["polyline"]["positions"]["references"] = ref






