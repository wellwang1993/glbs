from django.urls import path,include
from Polaris import views


from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'dnstype',views.Dnstypeinfo)
router.register(r'getidbydnsname/(?P<dnsname>.*)',views.GetIdByDnsname,base_name = 'dnsname')

router.register(r'dnszone',views.Dnszoneinfo)
#router.register(r'getidbyzone/(?P<zonename>.*)',views.GetIdByZone,base_name = 'zonename')
router.register(r'getidbyzone/(?P<sss>.*)',views.GetIdByZone)

router.register(r'nameidpolicy',views.NameidPolciyinfo)
router.register(r'getidbypolicyname/(?P<policyname>.*)',views.GetIdByPolicy,base_name = 'policyname')

router.register(r'vipdevice',views.VipDeviceinfo)
router.register(r'vipdevicetemp',views.VipDeviceTempinfo)
router.register(r'getidbyvipname/(?P<vipname>.*)',views.GetIdByVipdev,base_name = 'vipname')
router.register(r'getidbyvipnametemp/(?P<vipname>.*)',views.GetIdByVipdevTemp,base_name = 'vipname')

#对view的信息管理
router.register(r'viewtype',views.Viewtypeinfo)
router.register(r'view',views.Viewinfo)
router.register(r'getidbyfatherid/(?P<fatherid>[0-9]+)',views.GetIdByFatherid,base_name = 'viewid')

#对nameid的管理
router.register(r'nameid', views.Nameidinfo)
#通过域名获取域名id
router.register(r'getidbyname/(?P<nameid>.*)',views.NameidGetByName,base_name='nameid')


#对nameid view的管理
router.register(r'nameidview',views.NameidViewinfo)
router.register(r'getidbynameview/(?P<nameid>.*)/(?P<viewid>.*)',views.GetIdByNameidViewid,base_name = 'nameidview')
router.register(r'delbynameid',views.DelByNameid)
router.register(r'getitembynameid_inner/(?P<sss>.*)',views.GetItemBynameid_inner)

#对nameid view device的管理
router.register(r'nameidviewdevice',views.NameidViewDeviceinfo)
router.register(r'getdidbynameview/(?P<nameid>.*)/(?P<viewid>.*)',views.GetDIdByNameidViewid,base_name = 'dnameidview')
router.register(r'deldbynameid',views.DelDByNameid)
#通过nameid,viewid,deviceid获取记录
router.register(r'getidbynameviewdevice/(?P<nameid>.*)/(?P<viewid>.*)/(?P<deviceid>.*)',views.GetIdByNameidViewidDeviceid,base_name = 'nameidviewiddeviceid')
#通过域名id获取name,device信息
router.register(r'getnamedevinfo/(?P<sss>.*)',views.GetNameDevInfoByNameid)

#对cname的管理
router.register(r'cname',views.CnameInfo)
router.register(r'getidbyopsubu/(?P<operator>.*)/(?P<supplier>.*)/(?P<bussiness>.*)',views.GetItemByOpSuBu,base_name = 'opsubu')
#router.register(r'getidbycname/(?P<cname>.*)',views.GetIdByCname,base_name = 'cname')
#对nameid view cname的管理
router.register(r'nameidviewcname',views.NameidViewCnameinfo)
router.register(r'getcidbynameview/(?P<nameid>.*)/(?P<viewid>.*)',views.GetCIdByNameidViewid,base_name = 'cnameidview')
#通过nameid.viewid,cnameid查找记录
router.register(r'getcidbynameviewcname/(?P<nameid>.*)/(?P<viewid>.*)/(?P<cnameid>.*)',views.GetCIdByNameidViewidCnameid,base_name = 'nameidviewidcnameid')
router.register(r'getnamecnameinfo/(?P<sss>.*)',views.GetNameCnameInfoByNameid)


#对adminip的管理
router.register('adminip',views.AdminIpInfo)
#对探测任务的管理
router.register('detecttask',views.DetectTaskInfo)

#汇报数据可用性的接口
router.register('putdeviceavailability',views.DetectDeviceAvailabilityInfo)
#对设备可用性探测数据有效性的控制
router.register('deviceavailabilitystandard',views.DetectDeviceAvailabilityStandardInfo)
router.register(r'tests',views.testsss)

urlpatterns = [
   # path('ajax/GetRegion',views.GetRegion, name='ajax_GetRegion'),
    path('gettask/',views.url_get_vipaddress_from_cache),
    path('getnameid/',views.url_get_nameid_from_cache),
    path('', include(router.urls)),
]
from Polaris.init.gslb_init import scheduler
scheduler.start()
