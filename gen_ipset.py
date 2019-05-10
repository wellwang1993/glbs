# -*- coding:utf-8 -*-
import os
print(os.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GLB.settings")
import django
django.setup()

from Polaris.models import tb_fact_ori_view_info
from Polaris.utils.rawsql import my_custom_sql


view_id_dict = {}
def load_view_viewid():
    sql = "select id,view_country,view_isp,view_region,view_province,view_city from Polaris_tb_fact_temp_view_info where view_grade= 6"
    res = my_custom_sql(sql)
    for line in res:
        view_id = line[0]
        view_country = line[1]
        view_isp = line[2]
        view_region = line[3]
        view_province = line[4]
        view_city = line[5] 
        if view_country!= None and view_isp!= None and view_region!= None and view_province!= None and view_city !=None and view_country!="*" and view_isp!="*" and view_region !="*" and view_province!="*" and view_city !="*":
            view_id_dict["{}_{}_{}_{}_{}".format(view_country,view_isp,view_region,view_province,view_city)] = view_id
       
    
    sql = "select id,view_country,view_isp,view_region,view_province,view_city from Polaris_tb_fact_temp_view_info where view_grade= 5"
    res = my_custom_sql(sql)
    for line in res:
        view_id = line[0]
        view_country = line[1]
        view_isp = line[2]
        view_region = line[3]
        view_province = line[4]
        view_city = line[5] 
        if view_country!= None and view_isp!= None and view_region!= None and view_province!= None and view_country!="*" and view_isp!="*" and view_region !="*" and view_province!="*":
            if view_isp=="广电网" and view_province=="江苏":
                print(view_id)
            view_id_dict["{}_{}_{}_{}".format(view_country,view_isp,view_region,view_province)] = view_id
        

    sql = "select id,view_country,view_isp,view_region,view_province,view_city from Polaris_tb_fact_temp_view_info where view_grade= 4"
    res = my_custom_sql(sql)
    for line in res:
        view_id = line[0]
        view_country = line[1]
        view_isp = line[2]
        view_region = line[3]
        view_province = line[4]
        view_city = line[5] 
        if view_country!= None and view_isp!= None and view_region!= None and view_country!="*" and view_isp!="*" and view_region !="*":
            view_id_dict["{}_{}_{}".format(view_country,view_isp,view_region)] = view_id
        
    sql = "select id,view_country,view_isp,view_region,view_province,view_city from Polaris_tb_fact_temp_view_info where view_grade= 3"
    res = my_custom_sql(sql)
    for line in res:
        view_id = line[0]
        view_country = line[1]
        view_isp = line[2]
        view_region = line[3]
        view_province = line[4]
        view_city = line[5] 
        if view_country!= None and view_isp!= None and view_country!="*" and view_isp!="*":
            view_id_dict["{}_{}".format(view_country,view_isp)] = view_id
        
    sql = "select id,view_country,view_isp,view_region,view_province,view_city from Polaris_tb_fact_temp_view_info where view_grade= 2"
    res = my_custom_sql(sql)
    for line in res:
        view_id = line[0]
        view_country = line[1]
        view_isp = line[2]
        view_region = line[3]
        view_province = line[4]
        view_city = line[5] 
        if view_country!= None and view_country!="*":
            view_id_dict["{}".format(view_country)] = view_id

load_view_viewid()


def gen_ipset():
    sql = "select start_address,end_address,country,isp,region,province,city from Polaris_tb_fact_ori_view_info"
    res = my_custom_sql(sql)
    for line in res:
        view_start_address = line[0]
        view_end_address = line[1]
        view_country = line[2]
        view_isp = line[3]
        view_region = line[4]
        view_province = line[5]
        view_city = line[6]
        if view_country!= None and view_isp!= None and view_region!= None and view_province!= None and view_city !=None and view_country!="*" and view_isp!="*" and view_region !="*" and view_province!="*" and view_city !="*":
            view_id = view_id_dict.get("{}_{}_{}_{}_{}".format(view_country,view_isp,view_region,view_province,view_city))
        elif view_country!= None and view_isp!= None and view_region!= None and view_province!= None and view_country!="*" and view_isp!="*" and view_region !="*" and view_province!="*":
            view_id = view_id_dict.get("{}_{}_{}_{}".format(view_country,view_isp,view_region,view_province))
            if view_isp=="广电网" and view_province=="江苏":
                print("{}_{}_{}_{}_{}_{}_{}".format(view_id,view_start_address,view_end_address,view_country,view_isp,view_province,view_city))
        elif view_country!= None and view_isp!= None and view_region!= None and view_country!="*" and view_isp!="*" and view_region !="*":
            view_id = view_id_dict.get("{}_{}_{}".format(view_country,view_isp,view_region))
        elif view_country!= None and view_isp!= None and view_country!="*" and view_isp!="*":
            view_id = view_id_dict.get("{}_{}".format(view_country,view_isp))
        elif view_country!= None and view_country!="*":
            view_id = view_id_dict.get("{}".format(view_country)) 
        sql = 'insert into Polaris_tb_fact_ipset_info(view_id_id,start_address,end_address) values("{}","{}","{}")'.format(view_id,view_start_address,view_end_address)
        res = my_custom_sql(sql)
        print(sql)   
gen_ipset()      
