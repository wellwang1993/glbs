# -*- coding: utf-8 -*-
class address:
    def __init__(self):
        self.id = ""
        self.address = ""
        self.ratio = ""
    def gen_obj_dict(self,itemlist):
        objdict = {}
        if itemlist is not None:
            for item in itemlist:
                self.id = item.nameid_view_id.view_id
                self.address = item.nameid_device_id.vip_address
                self.ratio = item.nameid_device_ratio
                if objdict.get(self.id) == None:
                    objdict[self.id] = {}
                objdict[self.id][self.address] = self.ratio
        return objdict


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
    def genobj(self,obj_list,nameid_view_dict):
       # nameid_data_dict = {}
        nameid_name = obj_list[0]['nameid_id']['nameid_name']
        for item in obj_list:
            view_name = item["nameid_view_id"]["view_name"]
            if self.nameid_data_dict.get(view_name) == None:
                self.nameid_data_dict[view_name] = nameid_view_dict.get(item["nameid_view_id"]["view_id"])
            #self.nameid_data_dict[view_name]==None意味着在dimension_view_device或者dimension_view_cname中新增了view,但是在dimension_view中没有新增view.这样的逻辑是不对的
            if item.get("nameid_device_id") != None and self.nameid_data_dict.get(view_name) != None:
                self.nameid_data_dict[view_name].address[item["nameid_device_id"]["vip_address"]] = item["nameid_device_ratio"]
            if item.get("nameid_cname_id") != None and self.nameid_data_dict.get(view_name) != None:
                self.nameid_data_dict[view_name].cname[item["nameid_cname_id"]["nameid_cname"]] = item["nameid_cname_ratio"]
        return nameid_name
    def gen_default(self,obj):
        self.nameid_data_dict['default'] = obj.nameid_data_dict['default']
    def genobjs(self,item,nameid_view_dict):
        view_name = item["nameid_view_id"]["view_name"]
        if self.view.get(view_name) == None:
            self.view[view_name] = nameid_view_dict.get(item["nameid_view_id"]["view_id"])
        self.view[view_name].address[item["nameid_device_id"]["vip_address"]] = item["nameid_device_ratio"]
        return self
