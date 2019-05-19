# -*- coding:utf-8 -*-
import os
print(os.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GLB.settings")
import django
django.setup()

from Polaris.models import tb_fact_ori_view_info
from Polaris.utils.rawsql import my_custom_sql

def gen_default_view():
    sql = 'insert into Polaris_tb_fact_temp_view_info(view_father_id,view_default,view_grade_name,view_grade,view_father_grade,view_type_id) values(0,"default","default",1,0,1)'   
    res = my_custom_sql(sql)

def gen_country_view():
    sql = "select id,view_default from Polaris_tb_fact_temp_view_info where view_grade = 1"
    res = my_custom_sql(sql)
    default_view_dict = {}
    for line in res:
        view_id = line[0]
        view_default =  line[1]
        default_view_dict[view_default] = view_id
       
    sql = "select country from Polaris_tb_fact_ori_view_info group by country"
    res = my_custom_sql(sql)
    print(res)
    for line in res:
        view_country = line[0]
        view_father_id = default_view_dict.get("default")
        sql = 'insert into Polaris_tb_fact_temp_view_info(view_father_id,view_default,view_country,view_grade_name,view_grade,view_father_grade,view_type_id) values({},"default","{}","country",2,1,1)'.format(view_father_id,view_country)
        res = my_custom_sql(sql)
 
def gen_isp_view():
    sql = "select id,view_country from Polaris_tb_fact_temp_view_info where view_grade = 2" 
    res = my_custom_sql(sql)
    country_view_dict = {}    
    for line in res:
        view_id = line[0]
        view_country =  line[1]
        country_view_dict[view_country] = view_id
   
    sql = "select country,isp from Polaris_tb_fact_ori_view_info group by country,isp" 
    res = my_custom_sql(sql)
    for line in res:
        view_country = line[0]
        view_isp = line[1]
        view_father_id = country_view_dict.get(view_country)
        sql = 'insert into Polaris_tb_fact_temp_view_info(view_father_id,view_default,view_country,view_isp,view_grade_name,view_grade,view_father_grade,view_type_id) values({},"default","{}","{}","isp",3,2,1)'.format(view_father_id,view_country,view_isp) 
        res = my_custom_sql(sql)
#有些运营商只在一个大区有，有些运营商遍布所有大区，因此对应的region 就会多一些
def gen_region_view():
    '''
    region_province_dict = {
            "华东大区":["上海","江苏","浙江","安徽","江西","山东","福建","台湾"],
            "华北大区":["北京","天津","山西","河北","内蒙古"],
            "华中大区":["河南","湖北","湖南"],
            "华南大区":["广东","广西","海南","香港","澳门"],
            "西南大区":["四川","云南","贵州","西藏","重庆"],
            "西北大区":["陕西","甘肃","青海","宁夏","新疆"],
            "东北大区":["黑龙江","辽宁","吉林"]
    }
    for region,province_list in region_province_dict.items():
        for province in province_list:
            sql = 'update Polaris_tb_fact_ori_view_info set region = "{}" where province = "{}"'.format(region,province)
            print(sql)
            res = my_custom_sql(sql)
    '''
    sql = "select id,view_country,view_isp from Polaris_tb_fact_temp_view_info where view_grade = 3"
    res = my_custom_sql(sql)
    country_isp_dict = {}
    for line in res:
        view_id = line[0]
        view_country = line[1]
        view_isp = line[2]
        country_isp_dict["{}_{}".format(view_country,view_isp)] = view_id
        
    sql = "select country,isp,region from Polaris_tb_fact_ori_view_info group by country,isp,region" 
    res = my_custom_sql(sql)
    for line in res:
        view_country = line[0]
        view_isp = line[1]
        view_region = line[2] 
        view_father_id = country_isp_dict.get("{}_{}".format(view_country,view_isp))
        print(view_father_id)
        sql = 'insert into Polaris_tb_fact_temp_view_info(view_father_id,view_default,view_country,view_isp,view_region,view_grade_name,view_grade,view_father_grade,view_type_id) values({},"default","{}","{}","{}","region",4,3,1)'.format(view_father_id,view_country,view_isp,view_region)
        res = my_custom_sql(sql)

def gen_province_view():
    sql = "select id,view_country,view_isp,view_region from Polaris_tb_fact_temp_view_info where view_grade = 4"
    res = my_custom_sql(sql)
    country_isp_region_dict = {}
    for line in res:
        view_id = line[0]
        view_country = line[1]
        view_isp = line[2]
        view_region = line[3]
        country_isp_region_dict["{}_{}_{}".format(view_country,view_isp,view_region)] = view_id
    
    sql = "select country,isp,region,province from Polaris_tb_fact_ori_view_info group by country,isp,region,province"
    res = my_custom_sql(sql)
    for line in res:
        view_country = line[0]
        view_isp = line[1]
        view_region = line[2]
        view_province = line[3]
        view_father_id = country_isp_region_dict.get("{}_{}_{}".format(view_country,view_isp,view_region))
        sql = 'insert into Polaris_tb_fact_temp_view_info(view_father_id,view_default,view_country,view_isp,view_region,view_province,view_grade_name,view_grade,view_father_grade,view_type_id) values({},"default","{}","{}","{}","{}","province",5,4,1)'.format(view_father_id,view_country,view_isp,view_region,view_province)
        res = my_custom_sql(sql)

def gen_city_view():
    sql = "select id,view_country,view_isp,view_region,view_province from Polaris_tb_fact_temp_view_info where view_grade = 5"
    res = my_custom_sql(sql)
    country_isp_region_province_dict = {} 
    for line in res:
        view_id = line[0]
        view_country = line[1]
        view_isp = line[2]
        view_region = line[3]
        view_province = line[4]
        country_isp_region_province_dict["{}_{}_{}_{}".format(view_country,view_isp,view_region,view_province)] = view_id
    sql = "select country,isp,region,province,city from Polaris_tb_fact_ori_view_info group by country,isp,region,province,city"
    res = my_custom_sql(sql)
    for line in res:
        view_country = line[0]
        view_isp = line[1]
        view_region = line[2]
        view_province = line[3]
        view_city = line[4]
        view_father_id = country_isp_region_province_dict.get("{}_{}_{}_{}".format(view_country,view_isp,view_region,view_province))
        sql = 'insert into Polaris_tb_fact_temp_view_info(view_father_id,view_default,view_country,view_isp,view_region,view_province,view_city,view_grade_name,view_grade,view_father_grade,view_type_id) values({},"default","{}","{}","{}","{}","{}","city",6,5,1)'.format(view_father_id,view_country,view_isp,view_region,view_province,view_city)
        res = my_custom_sql(sql)

#gen_city_view()
#gen_province_view()
#gen_region_view()
#gen_isp_view()
#gen_country_view()
#gen_default_view()
