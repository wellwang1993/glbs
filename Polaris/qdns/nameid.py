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
    '''
    def genobjs(self,obj_list,nameid_view_dict):
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
    '''
    def genobj(self,obj_list,nameid_view_dict):
        nameid_name = obj_list[0]['nameid_id']['nameid_name']
        for item in obj_list:
            #view_id = item["nameid_view_id"]["id"]
            view_id = []
            view_default = item["nameid_view_id"]['view_default']
            view_country = item["nameid_view_id"]['view_country']
            if view_country:
                view_id.append(view_country)
            view_isp = item["nameid_view_id"]['view_isp'] 
            if view_isp:
                view_id.append(view_isp)
            view_region = item["nameid_view_id"]['view_region']
            if view_region:
                view_id.append(view_region)
            view_province = item["nameid_view_id"]['view_province']
            if view_province:
                view_id.append(view_province)
            view_city = item["nameid_view_id"]['view_city']
            if view_city:
                view_id.append(view_city)
            if len(view_id) ==0:
                view_id = view_default
            else:
                view_id = '_'.join(view_id)
            if self.nameid_data_dict.get(view_id) == None:
                self.nameid_data_dict[view_id] = nameid_view_dict.get(item["nameid_view_id"]["id"]) 
            if item.get("nameid_device_id") != None and self.nameid_data_dict.get(view_id) != None:
                self.nameid_data_dict[view_id].address[item["nameid_device_id"]["vip_address"]] = item["nameid_device_ratio"]
            if item.get("nameid_cname_id") != None and self.nameid_data_dict.get(view_id) != None:
                self.nameid_data_dict[view_id].cname[item["nameid_cname_id"]["nameid_cname"]] = item["nameid_cname_ratio"]
        return nameid_name
