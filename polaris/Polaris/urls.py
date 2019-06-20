from django.urls import path,include
from Polaris import views


from rest_framework.routers import DefaultRouter
router = DefaultRouter()

#对dns类型的管理
router.register(r'dnstype',views.Dnstypeinfo)
#对dnsip的管理
router.register(r'dnsip',views.DnsIpinfo)
#对zone类型的管理
router.register(r'zonetype',views.Zonetypeinfo)
#对zone文件的管理
router.register(r'dnszone',views.Dnszoneinfo)
#对策略的管理
router.register(r'nameidpolicy',views.NameidPolciyinfo)
#对虚拟设备的管理
router.register(r'vipdevice',views.VipDeviceinfo)

#对view的信息管理
router.register(r'viewtype',views.Viewtypeinfo)
router.register(r'view',views.Viewinfo)
#对nameid的管理
router.register(r'nameid', views.Nameidinfo)

#对nameid view的管理
router.register(r'nameidview',views.NameidViewinfo)

#对nameid view device的管理
router.register(r'nameidviewdevice',views.NameidViewDeviceinfo)

#对cname的管理
router.register(r'cname',views.CnameInfo)
#对nameid view cname的管理
router.register(r'nameidviewcname',views.NameidViewCnameinfo)

#对adminip的管理
router.register('adminip',views.AdminIpInfo)
#对探测任务的管理
router.register('detecttask',views.DetectTaskInfo)

#汇报数据可用性的接口
router.register('putdeviceavailability',views.DetectDeviceAvailabilityInfo,base_name='putdevice')
#展示数据的
router.register('showputdeviceavailability',views.ShowDetectDeviceAvailabilityInfo)

#对设备可用性探测数据有效性的控制
router.register('deviceavailabilitystandard',views.DetectDeviceAvailabilityStandardInfo)


urlpatterns = [
    path('gettask/',views.url_get_vipaddress_from_cache),
    path('getnameid/',views.url_get_nameid_from_cache),
    path('getzone/',views.url_get_zone_from_cache),
    path('getdnstype/',views.url_get_dnstype_from_cache),
    path('', include(router.urls)),
]
from Polaris.init.gslb_init import scheduler
scheduler.start()
