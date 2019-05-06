from Polaris.utils.rawsql import my_custom_sql
from Polaris.utils.glbscache import read_from_cache,write_to_cache
from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster
import logging
logger = logging.getLogger('dj')
import json

#生成探测任务的
#这里Polaris_tb_fact_device_info在筛选的过程中，没有把它的状态考虑进来，因为如果下线的时候肯定会设置为disable，那么最终这台设备的状态就是disable的，这样的话最终在生成配置文件的时候会把设备剔除掉，当然这是自动探测最好的时候
def load_detect_vipdevice_cache():
    sql = "select detect_frency from Polaris_tb_fact_detecttask_info where detect_name='detect_device_availability'"
    res = my_custom_sql(sql)
    frequency = 15
    for item in res:
        frequency = item[0]
    sql = "select a.admin_ip,b.vip_address,a.isp,a.status from Polaris_tb_fact_adminip_info as a left join Polaris_tb_fact_device_info as b on a.isp =b.node_isp" 
    res = my_custom_sql(sql)
    #logger.info(type(res))
    #logger.info(res)
    raw_vip = {}
    for item in res:
        adminip = item[0]
        vip = item[1]
        isp = item[2]
        status = item[3]
        if raw_vip.get(adminip) == None:
            raw_vip[adminip] = {}
            raw_vip[adminip]["vip_address"] = []
            raw_vip[adminip]["adminip_isp"] = isp
            raw_vip[adminip]["detect_switch"] = status
            raw_vip[adminip]["frequency"] = frequency
        raw_vip[adminip]["vip_address"].append(vip)
    for item in raw_vip:
        write_to_cache_cluster("vipdevice","detect-vipaddress",item,json.dumps(raw_vip[item]))
        #logger.info(read_from_cache(item))

#加载设备可用性的
def load_device_availability_cache():
    sql = "select node_isp,total_value,absolute_value,relative_rate from Polaris_tb_fact_detectdeviceavailability_standard_info"
    res = my_custom_sql(sql)
    isp_standard_data = {}
    for item in res:
        isp = item[0]
        total_value = item[1]
        absolute_value = item[2]
        relative_rate = item[3]
        if isp_standard_data.get(isp) == None:
            isp_standard_data[isp] = {}
        isp_standard_data[isp]["total_value"] = total_value
        isp_standard_data[isp]["absolute_value"] = absolute_value
        isp_standard_data[isp]["relative_rate"] = relative_rate

    sql = "select vip_address,availability,admin_isp,count(availability) from Polaris_tb_fact_detectdeviceavailability_info where create_time >= DATE_FORMAT(DATE_ADD(now(), INTERVAL - 1 MONTH),'%y-%m-%d %H:%i') group by vip_address,availability"
    res = my_custom_sql(sql)
    vip_avil_dict = {}
    for item in res:
        vip_address = item[0]
        status = item[1]
        admin_isp = item[2]
        num = item[3]
        #设备的运营商信息以最后一次为准
        if vip_avil_dict.get(vip_address) == None:
            vip_avil_dict[vip_address] = [status,num,admin_isp]
        elif vip_avil_dict[vip_address][1] < num:
            vip_avil_dict[vip_address][0] = status
            vip_avil_dict[vip_address][1] = vip_avil_dict[vip_address][1]+num
            vip_avil_dict[vip_address][2] = admin_isp
        else:    
            vip_avil_dict[vip_address][1] = vip_avil_dict[vip_address][1]+num
            vip_avil_dict[vip_address][2] = admin_isp

        #if vip_avil_dict.get(vip_address) == None or vip_avil_dict[vip_address][1] < num:
        #    vip_avil_dict[vip_address] = [status,num,admin_isp]
    #会有三种状态，对于数据不符合检验标准的，都认为是无效的，对于无效的探测数据，还是要采用手工配置的方式
    for item in vip_avil_dict:
        status = vip_avil_dict[item][0]
        num = vip_avil_dict[item][1]
        admin_isp = vip_avil_dict[item][2]
        logger.info("{}*****{}******{}******{}".format(item,status,num,admin_isp))
        if isp_standard_data.get(admin_isp) == None:
            write_to_cache_cluster("vipdevice","detect-vipaddress-availability",item,"invalid") 
            logger.info("{}********{}".format(item,read_from_cache_cluster("vipdevice","detect-vipaddress-availability",item)))
        else:
            total_value = isp_standard_data[admin_isp]["total_value"]
            absolute_value = isp_standard_data[admin_isp]["absolute_value"]
            relative_rate = isp_standard_data[admin_isp]["relative_rate"]
            logger.info("{}&&&&&&&&{}&&&&&&&&{}&&&&&&&{}&&&&&&&&&{}".format(item,num,absolute_value,num / total_value,relative_rate))
            if num < absolute_value or (num / total_value < relative_rate):
                write_to_cache_cluster("vipdevice","detect-vipaddress-availability",item,"invalid") 
            else:
                write_to_cache_cluster("vipdevice","detect-vipaddress-availability",item,vip_avil_dict[item][0])

            logger.info("{}********{}".format(item,read_from_cache_cluster("vipdevice","detect-vipaddress-availability",item)))



        '''
        #如果这里关闭设备开关的话表面设备的可用性状态需要手工去指定，而不是通过探测数据指定
        dev_switch = read_from_cache_cluster("vipdevice","devswitch",item)
        logger.info("{}========{}".format(item,type(dev_switch)))
        if dev_switch is not None:
            dev_switch_str = str(dev_switch,encoding = "utf8")
            dev_switch = dev_switch_str.split("-") 
            if len(dev_switch) == 2 and dev_switch[1] == "disable":
                write_to_cache_cluster("vipdevice","vipaddress-availability",item,dev_switch[0])
            else:
                write_to_cache_cluster("vipdevice","vipaddress-availability",item,vip_avil_dict[item][0])
        else:
            write_to_cache_cluster("vipdevice","vipaddress-availability",item,vip_avil_dict[item][0])
        '''
#加载设备是否采用探测数据，以及手动设置设备可用性,相当于开关
def load_device_switch_cache():
    sql = 'select vip_address,vip_status,vip_enable_switch from Polaris_tb_fact_device_info'
    res = my_custom_sql(sql)
    vip_avil_dict = {}
    for item in res:
        vip_address = item[0]
        vip_status = item[1]
        vip_enable_switch = item[2]
        
        if vip_enable_switch == "enable":
            detect_vip_availability = read_from_cache_cluster("vipdevice","detect-vipaddress-availability",vip_address)
            logger.info("{}$$$$$$${}$$$$${}".format(vip_address,vip_enable_switch,detect_vip_availability))
            if detect_vip_availability == "enable" or detect_vip_availability == "disable":
                write_to_cache_cluster("vipdevice","vipaddress-availability",vip_address,detect_vip_availability)
            else:
                write_to_cache_cluster("vipdevice","vipaddress-availability",vip_address,vip_status)
        else:
            write_to_cache_cluster("vipdevice","vipaddress-availability",vip_address,vip_status)
        logger.info("{}==={}==={}".format(vip_address,vip_status,read_from_cache_cluster("vipdevice","vipaddress-availability",vip_address)))
