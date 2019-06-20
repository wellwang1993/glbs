from Polaris.utils.rawsql import my_custom_sql
import logging
logger = logging.getLogger('qdns_dnstype_access')
import json

def get_dnstype_from_cache(address):
    logger.info("the {} qdns get dnstype ".format(address))
    sql = 'select b.dns_name from Polaris_tb_fact_dnsip_info a left join Polaris_tb_fact_dnstype_info b on a.dns_type_id = b.id where dns_ip = "{}"'.format(address)
    res = my_custom_sql(sql)    
    if res != None and len(res) != 0:
        for item in res:
            dnstype = item[0]
            if dnstype != None:
                return dnstype
    return ""

