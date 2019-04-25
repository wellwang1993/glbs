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
        self.cname = ""
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
            self.nameid_data_dict[view_name].address[item["nameid_device_id"]["vip_address"]] = item["nameid_device_ratio"]
        return nameid_name
    def genobjs(self,item,nameid_view_dict):
        view_name = item["nameid_view_id"]["view_name"]
        if self.view.get(view_name) == None:
            self.view[view_name] = nameid_view_dict.get(item["nameid_view_id"]["view_id"])
        self.view[view_name].address[item["nameid_device_id"]["vip_address"]] = item["nameid_device_ratio"]
        return self
