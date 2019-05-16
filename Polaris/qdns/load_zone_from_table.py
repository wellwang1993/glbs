
from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster,delete_to_cache_cluster,read_from_cache_cluster,get_keys_from_cache
from Polaris.models import tb_fact_nameid_info,tb_fact_dnszone_info
from Polaris.utils.rawsql import my_custom_sql
import logging
logger = logging.getLogger('qdns_zone_config')
import json

def load_zone_from_table():
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
                 sql = 'select zone_name,record_name,record_content,internet_type,record_type,record_ttl from Polaris_tb_fact_dnszone_info where dns_type_id = "{}"'.format(id)
                 zoneres = my_custom_sql(sql)
                 if zoneres != None and len(zoneres) !=0:
                     zonename_tag = False
                     for zoneitem in zoneres:
                         zone_name = zoneitem[0]
                         if nameid.find(zone_name) != -1:
                             zonename_tag = True
                         record_name = zoneitem[1]
                         record_content = zoneitem[2]
                         internet_type = zoneitem[3]
                         record_type = zoneitem[4]
                         record_ttl = zoneitem[5]
                         if zoneqdns_dict.get(dnsname) == None:
                             zoneqdns_dict[dnsname] = {}
                         if zoneqdns_dict[dnsname].get(zone_name) == None:
                             zoneqdns_dict[dnsname][zone_name] = []
                         zoneqdns_dict[dnsname][zone_name].append({"record_name":record_name,"record_content":record_content,"internet_type":internet_type,"record_type":record_type,"record_ttl":record_ttl})
                     if len(zoneqdns_dict) == 0 or zonename_tag == False:
                         logger.info("the nameid zone is not legal,the nameid is {}".format(nameid))
    if len(zoneqdns_dict) == 0:
        logger.info("the zone dict is null")
    keys = get_keys_from_cache("vipdevice","zone-config")
    for key in keys:
        key = str(key,encoding = "raw_unicode_escape")
        if zoneqdns_dict.get(key) == None:
            logger.info("the nameid {} is disable".format(key))
            delete_to_cache_cluster("vipdevice","zone-config",key) 
    for dnstype,zoneinfo in zoneqdns_dict.items():
        logger.info("the dnstype is {},the zone info is {}".format(dnstype,json.dumps(zoneinfo)))
        write_to_cache_cluster("vipdevice","zone-config",str(dnstype),json.dumps(zoneinfo))
