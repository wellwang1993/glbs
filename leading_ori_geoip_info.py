# -*- coding:utf-8 -*-
import os
print(os.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GLB.settings") 
import django
django.setup()

path = "ipv4_pro_cn.txtx"
def leading_ori_geoip_info():
    geoip_list = []
    idx=0
    with open(path,"r") as f:
        from Polaris.models import tb_fact_ori_view_info
        for line in f.readlines():
            print(line)
            if line != None:
                line_list = line.split("\t")
                if line_list[2] == "中国":
                    obj = tb_fact_ori_view_info.objects.create(start_address = line_list[0],end_address = line_list[1],country = line_list[2],province=line_list[3],city=line_list[4],unknow_a =line_list[5],isp=line_list[6])
                    geoip_list.append(obj)
                    print(idx)
                    idx=idx+1
    
    f.close()
    tb_fact_ori_view_info.objects.bulk_create(geoip_list)
leading_ori_geoip_info()
