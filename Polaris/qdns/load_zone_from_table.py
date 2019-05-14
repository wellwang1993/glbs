
from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster,delete_to_cache_cluster
#from Polaris.models import tb_fact_nameid_info,tb_fact_dnszone_info
from Polaris.utils.rawsql import my_custom_sql
import logging
logger = logging.getLogger('qdns_zone_config')
import json

def load_zone_from_table():
    pass
'''
    zoneqdns_dict = {}
    objs = tb_fact_nameid_info.objects.all()
    for obj in objs:
         nameid = obj.nameid_name
         status = obj.nameid_status
         if status != "enable":
             continue
         sql = 'select a.dns_type_id,b.dns_name from Polaris_tb_fact_nameid_info a left join Polaris_tb_fact_dnstype_info b on a.dns_type_id = b.id where nameid_name = "{}"'.format(nameid)
         res = my_custom_sql(sql)         
         if res != None and len(res) != 0:
             for item in res:
                 id = item[0]
                 dnsname = item[1]
                 sql = 'select zone_name,zone_soa,ns_name,ns_address,ns_ttl from Polaris_tb_fact_dnszone_info where dns_type_id = "{}"'.format(id)
                 zoneres = my_custom_sql(sql)
                 if zoneres != None and len(zoneres) !=0:
                     zonename_tag = False
                     for zoneitem in zoneres:
                         zone_name = zoneitem[0]
                         if nameid.find(zone_name) != -1:
                             zonename_tag = True
                         zone_soa = zoneitem[1]
                         ns_name = zoneitem[2]
                         ns_address = zoneitem[3]
                         ns_ttl = zoneitem[4]
                         if zoneqdns_dict.get(dnsname) == None:
                             zoneqdns_dict[dnsname] = {}
                         if zoneqdns_dict[dnsname].get(zone_name) == None:
                             zoneqdns_dict[dnsname][zone_name] = []
                         zoneqdns_dict[dnsname][zone_name].append({"zone_soa":zone_soa,"ns_name":ns_name,"ns_address":ns_address,"ns_ttl":ns_ttl})
                     if len(zoneqdns_dict) == 0 or zonename_tag == False:
                         logger.info("the nameid zone is not legal,the nameid is {}".format(nameid))
    if len(zoneqdns_dict) == 0:
        logger.info("the zone dict is null")
    for dnstype,zoneinfo in zoneqdns_dict.items():
        logger.info("the dnstype is {},the zone info is {}".format(dnstype,json.dumps(zoneinfo)))
        write_to_cache_cluster("vipdevice","zone-config",str(dnstype),json.dumps(zoneinfo)) 
''' 
