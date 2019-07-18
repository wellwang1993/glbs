from Polaris.utils.rawsql import my_custom_sql
from Polaris.utils.glbscache import read_from_cache,write_to_cache
from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster,get_keys_from_cache,delete_to_cache_cluster
import logging
logger = logging.getLogger('vipdevice_availability_data')
import json

#生成探测任务的
#这里Polaris_tb_fact_device_info在筛选的过程中，没有把它的状态考虑进来，因为如果下线的时候肯定会设置为disable，那么最终这台设备的状态就是disable的，这样的话最终在生成配置文件的时候会把设备剔除掉，当然这是自动探测最好的时候
def gen_detect_viplist_cache():
    try:
        sql = "select detect_frency,detect_frency_unit from Polaris_tb_fact_detecttask_info where detect_name='detect_device_availability'"
        res = my_custom_sql(sql)
        frequency = 15
        frequency_unit = 'second'
        for item in res:
            frequency = item[0]
            frequency_unit = item[1]
            if frequency == None or frequency_unit == None:
                frequency = 15
                frequency_unit = 'second'
        sql = "select a.admin_ip,b.vip_address,a.isp,a.availability_status from Polaris_tb_fact_adminip_info as a left join Polaris_tb_fact_device_info as b on a.isp =b.node_isp" 
        res = my_custom_sql(sql)
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
            #    raw_vip[adminip]["frequency_unit"] = frequency_unit
                
            raw_vip[adminip]["vip_address"].append(vip)
        keys = get_keys_from_cache("vipdevice","detect-vipaddress")
        for key in keys:
            key = str(key,encoding = "raw_unicode_escape")
            if raw_vip.get(key) == None:
                logger.info("the adminip {} is disable".format(key))
                delete_to_cache_cluster("vipdevice","detect-vipaddress",key)
        for item in raw_vip:
            write_to_cache_cluster("vipdevice","detect-vipaddress",item,json.dumps(raw_vip[item]))
            logger.info("adminip is {},detect vip is {} ".format(item,read_from_cache_cluster("vipdevice","detect-vipaddress",item)))
    except Exception as err:
        logger.error(err)
#加载探测数据确认设备的可用性
def load_device_availability_cache():
    try:
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
        
        sql = "select effective_time,effective_time_unit from Polaris_tb_fact_detecttask_info where detect_name='detect_device_availability'"
        res = my_custom_sql(sql)
        effective_time = 15
        effective_time_unit = 'second'
        for item in res:
            effective_time = item[0]
            effective_time_unit = item[1]
            if effective_time == None or effective_time_unit == None:
                effective_time = 15
                effective_time_unit = 'second'
        #这里group by vip和availability，以vip为key,拿到最终上报的关于该vip的总的探针个数，上报的状态，以及运营商
        sql = 'select vip_address,availability,admin_isp,count(availability) from Polaris_tb_fact_detectdeviceavailability_select_info where create_time >= DATE_FORMAT(DATE_ADD(now(), INTERVAL - {} {}),"%y-%m-%d %H:%i:%s") group by vip_address,availability'.format(effective_time,effective_time_unit)
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
        
        detect_vip_status = {}
        #if vip_avil_dict.get(vip_address) == None or vip_avil_dict[vip_address][1] < num:
        #    vip_avil_dict[vip_address] = [status,num,admin_isp]
        #开始确定每个vip的状态,对于每个vip都要满足俩个标准，一个是上报的探针个数要达到那个绝对值，还有一个是要达到那个相对值,会有三种状态，对于数据不符合检验标准的，都认为是无效的，对于无效的探测数据，还是要采用手工配置的方式
        for item in vip_avil_dict:
            status = vip_avil_dict[item][0]
            num = vip_avil_dict[item][1]
            admin_isp = vip_avil_dict[item][2]
            if isp_standard_data.get(admin_isp) == None:
                detect_vip_status[item] = "invalid"
                #write_to_cache_cluster("vipdevice","detect-vipaddress-availability",item,"invalid") 
            else:
                total_value = isp_standard_data[admin_isp]["total_value"]
                absolute_value = isp_standard_data[admin_isp]["absolute_value"]
                relative_rate = isp_standard_data[admin_isp]["relative_rate"]
                logger.info("the vip is {},the total detect alive vip num is {},the standared num is {},the relative percent alive is {},the standared is {}".format(item,num,absolute_value,num / total_value,relative_rate))
                if num < absolute_value or (num / total_value < relative_rate):
                    detect_vip_status[item] = "invalid"
                    #write_to_cache_cluster("vipdevice","detect-vipaddress-availability",item,"invalid") 
                else:
                    detect_vip_status[item] = vip_avil_dict[item][0]
                    #write_to_cache_cluster("vipdevice","detect-vipaddress-availability",item,vip_avil_dict[item][0])
                logger.info("the vip {},the detect status is {}".format(item,read_from_cache_cluster("vipdevice","detect-vipaddress-availability",item)))
        keys = get_keys_from_cache("vipdevice","detect-vipaddress-availability")
        for key in keys:
            key = str(key,encoding = "raw_unicode_escape")
            if detect_vip_status.get(key) ==None:
                logger.info("the detect vip {} is disable".format(key))
                delete_to_cache_cluster("vipdevice","detect-vipaddress-availability",key)
        for vip,status in detect_vip_status.items():
            write_to_cache_cluster("vipdevice","detect-vipaddress-availability",vip,status)
    except Exception as err:
        logger.error(err)
#结合设备的开关和探测数据，设置虚拟设备最终的状态，包括disable,enable,invalid
def generate_device_status_cache():
    try:
        sql = 'select vip_address,vip_status,vip_enable_switch from Polaris_tb_fact_device_info'
        res = my_custom_sql(sql)
        vip_avil_dict = {}
        for item in res:
            vip_address = item[0]
            vip_status = item[1]
            vip_enable_switch = item[2]
        
            if vip_enable_switch == "enable":
                detect_vip_availability = read_from_cache_cluster("vipdevice","detect-vipaddress-availability",vip_address)
                if detect_vip_availability == "enable" or detect_vip_availability == "disable":
                    #write_to_cache_cluster("vipdevice","vipaddress-availability",vip_address,detect_vip_availability)
                    vip_avil_dict[vip_address] = detect_vip_availability
                else:
                    vip_avil_dict[vip_address] = vip_status
                    #write_to_cache_cluster("vipdevice","vipaddress-availability",vip_address,vip_status)
            else:
                vip_avil_dict[vip_address] = vip_status
                #write_to_cache_cluster("vipdevice","vipaddress-availability",vip_address,vip_status)
            logger.info("the vip {},the vip_enable_switch is {},the vip_status is {},the detect status is {}".format(vip_address,vip_enable_switch,vip_status,read_from_cache_cluster("vipdevice","vipaddress-availability",vip_address)))
        keys = get_keys_from_cache("vipdevice","vipaddress-availability")
        for key in keys:
            key = str(key,encoding = "raw_unicode_escape")
            if vip_avil_dict.get(key) == None:
                logger.info("the vip {} is disable".format(key))
                delete_to_cache_cluster("vipdevice","vipaddress-availability",key)
        for vip,status in vip_avil_dict.items():
            write_to_cache_cluster("vipdevice","vipaddress-availability",vip,status)
    except Exception as err:
        logger.error(err)
