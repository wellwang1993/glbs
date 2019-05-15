from django.urls import path,include
from Polaris import views


from rest_framework.routers import DefaultRouter
router = DefaultRouter()
#对dns类型的管理
router.register(r'dnstype',views.Dnstypeinfo)
router.register(r'getidbydnsname/(?P<dnsname>.*)',views.GetIdByDnsname,base_name = 'dnsname')
#对zone文件的管理
router.register(r'dnszone',views.Dnszoneinfo)
router.register(r'getidbyzone/(?P<zonename>.*)',views.GetIdByZone,base_name = 'zonename')
#对策略的管理
router.register(r'nameidpolicy',views.NameidPolciyinfo)
router.register(r'getidbypolicyname/(?P<policyname>.*)',views.GetIdByPolicy,base_name = 'policyname')
#对虚拟设备的管理
router.register(r'vipdevice',views.VipDeviceinfo)
router.register(r'getidbyvipname/(?P<vipname>.*)',views.GetIdByVipdev,base_name = 'vipname')
#批量更新节点的状态
router.register(r'updatedevbynode/(?P<nodeid>.*)/(?P<status>.*)',views.UpdateDevByNodeid,base_name = 'nodeid')

#对view的信息管理
router.register(r'viewtype',views.Viewtypeinfo)
router.register(r'view',views.Viewinfo)
router.register(r'getidbyfatherid/(?P<fatherid>[0-9]+)',views.GetIdByFatherid,base_name = 'viewid')
router.register(r'getidbyviewinfo/(?P<country>.*)/(?P<isp>.*)/(?P<region>.*)/(?P<province>.*)/(?P<city>.*)',views.GetIdByViewInfo,base_name = 'viewidinfo')
#对nameid的管理
router.register(r'nameid', views.Nameidinfo)
#通过域名获取域名id
router.register(r'getidbyname/(?P<nameid>.*)',views.NameidGetByName,base_name='nameid')

#对nameid view的管理
router.register(r'nameidview',views.NameidViewinfo)
router.register(r'getidbynameview/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)',views.GetIdByNameidViewid,base_name = 'nameidview')
router.register(r'delbynameid',views.DelByNameid)
#通过域名id获取view信息
router.register(r'getitembynameid_inner/(?P<nameid>[0-9]+)',views.GetItemBynameid_inner,base_name='nameidviewinner')


#对nameid view device的管理
router.register(r'nameidviewdevice',views.NameidViewDeviceinfo)
router.register(r'getdidbynameview/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)',views.GetDIdByNameidViewid,base_name = 'dnameidview')
router.register(r'deldbynameid',views.DelDByNameid)
#通过nameid,viewid,deviceid获取记录
router.register(r'getidbynameviewdevice/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)/(?P<deviceid>[0-9]+)',views.GetIdByNameidViewidDeviceid,base_name = 'nameidviewiddeviceid')
#通过域名id获取name,device信息
router.register(r'getnamedevinfo/(?P<nameid>[0-9]+)',views.GetNameDevInfoByNameid,base_name='nameid')

#对cname的管理
router.register(r'cname',views.CnameInfo)
router.register(r'getidbyopsubu/(?P<operator>.*)/(?P<supplier>.*)/(?P<bussiness>.*)',views.GetItemByOpSuBu,base_name = 'opsubu')
#router.register(r'getidbycname/(?P<cname>.*)',views.GetIdByCname,base_name = 'cname')
#对nameid view cname的管理
router.register(r'nameidviewcname',views.NameidViewCnameinfo)
router.register(r'getcidbynameview/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)',views.GetCIdByNameidViewid,base_name = 'cnameidview')
#通过nameid.viewid,cnameid查找记录
router.register(r'getcidbynameviewcname/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)/(?P<cnameid>[0-9]+)',views.GetCIdByNameidViewidCnameid,base_name = 'nameidviewidcnameid')
#通过域名id获取view,cname信息
router.register(r'getnamecnameinfo/(?P<nameid>[0-9]+)',views.GetNameCnameInfoByNameid,base_name='nameidcname')


#对adminip的管理
router.register('adminip',views.AdminIpInfo)
#对探测任务的管理
router.register('detecttask',views.DetectTaskInfo)

#汇报数据可用性的接口
router.register('putdeviceavailability',views.DetectDeviceAvailabilityInfo)
#对设备可用性探测数据有效性的控制
router.register('deviceavailabilitystandard',views.DetectDeviceAvailabilityStandardInfo)

urlpatterns = [
    path('gettask/',views.url_get_vipaddress_from_cache),
    path('getnameid/',views.url_get_nameid_from_cache),
    path('getzone/',views.url_get_zone_from_cache),
    path('', include(router.urls)),
]
from Polaris.init.gslb_init import scheduler
scheduler.start()
