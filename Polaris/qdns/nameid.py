# -*- coding: utf-8 -*-
import copy
class ViewClass:
    def __init__(self):
        self.preferred = ""
        self.ttl = ""
        self.maxip = ""
        self.resolve_type = ""
        self.address = {}
        self.cname = {}
    def genobj(self,item):
        self.preferred = item["nameid_preferred"]
        self.ttl = item["nameid_ttl"]
        self.maxip = item["nameid_max_ip"]
        self.resolve_type = item["nameid_resolve_type"]
        return self
class NameidClass:
    def __init__(self):
        self.nameid_data_dict = {}
        self.default_dict = {}
    def __str__(self):
        return self

    def genobj(self,obj_list,nameid_view_dict):
        nameid_name = obj_list[0]['nameid_id']['nameid_name']
        for item in obj_list:
            view_id = item["nameid_view_id"]["id"]
            if self.nameid_data_dict.get(view_id) == None:
                self.nameid_data_dict[view_id] = nameid_view_dict.get(item["nameid_view_id"]["id"]) 
            if item.get("nameid_device_id") != None and self.nameid_data_dict.get(view_id) != None:
                self.nameid_data_dict[view_id].address[item["nameid_device_id"]["vip_address"]] = item["nameid_device_ratio"]
            if item.get("nameid_cname_id") != None and self.nameid_data_dict.get(view_id) != None:
                self.nameid_data_dict[view_id].cname[item["nameid_cname_id"]["nameid_cname"]] = item["nameid_cname_ratio"]
        return nameid_name
