from glbs.utils.rawsql import my_custom_sql
from glbs.utils.glbscache import read_from_cache,write_to_cache
from glbs.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster
import logging
logger = logging.getLogger('dj')
import json

#生成探测任务的
def load_detect_vipdevice_cache():
    sql = "select a.admin_ip,b.vip_address,a.isp from glbs_tb_fact_adminip_info as a left join glbs_tb_fact_device_info as b on a.isp =b.node_isp where a.status='enable'" 
    res = my_custom_sql(sql)
    #logger.info(type(res))
    #logger.info(res)
    raw_vip = {}
    for item in res:
        adminip = item[0]
        vip = item[1]
        if raw_vip.get(adminip) == None:
            raw_vip[adminip] = []
        raw_vip[adminip].append(vip)
    for item in raw_vip:
        write_to_cache(item,json.dumps(raw_vip[item])) 
        #logger.info(read_from_cache(item))

#加载设备可用性的
def load_device_availability_cache():
    sql = "select vip_address,availability,count(availability) from glbs_tb_fact_detectdeviceavailability_info where create_time >= DATE_FORMAT(DATE_ADD(now(), INTERVAL - 1 DAY),'%y-%m-%d %H:%i') group by vip_address,availability"
    res = my_custom_sql(sql)
    vip_avil_dict = {}
    for item in res:
        vip_address = item[0]
        status = item[1]
        num = item[2]
        if vip_avil_dict.get(vip_address) == None or vip_avil_dict[vip_address][1] < num:
            vip_avil_dict[vip_address] = [status,num]
            
  
    for item in vip_avil_dict:
        #如果这里关闭设备开关的话表面设备的可用性状态需要手工去指定，而不是通过探测数据指定
        dev_switch = read_from_cache_cluster("vipdevice","devswitch",item)
        logger.info("{}========{}".format(item,dev_switch))
        if dev_switch is not None:
            dev_switch = list(dev_switch)
            if len(dev_switch) == 2 and dev_switch[1] == "disable":
                write_to_cache(item,dev_switch[0])
            else:
                write_to_cache(item,vip_avil_dict[item][0])
        else:
            write_to_cache(item,vip_avil_dict[item][0])
        logger.info("***********")
        logger.info("{}////{}".format(dev_switch,"hkkkkkkkkkk"))
        logger.info(item)
        logger.info(read_from_cache(item))

#加载设备是否采用探测数据，以及手动设置设备可用性,相当于开关
def load_device_switch_cache():
    sql = 'select vip_address,vip_status,vip_enable_switch from glbs_tb_fact_device_info'
    res = my_custom_sql(sql)
    vip_avil_dict = {}
    for item in res:
        vip_address = item[0]
        vip_status = item[1]
        vip_enable_switch = item[2]
        write_to_cache_cluster("vipdevice",vip_address,''.join([vip_status,vip_enable_switch]))
        logger.info("{}==={}==={}".format(vip_address,vip_status,vip_enable_switch))
        logger.info(read_from_cache_cluster("vipdevice",vip_address))
