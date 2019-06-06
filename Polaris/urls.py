from django.urls import path,include
from Polaris import views


from rest_framework.routers import DefaultRouter
vip_router = DefaultRouter()
router = DefaultRouter()
#对dns类型的管理
router.register(r'dnstype',views.Dnstypeinfo)
router.register(r'getidbydnsname/(?P<dnsname>.*)',views.GetIdByDnsname,base_name = 'dnsname')
#对dnsip的管理
router.register(r'dnsip',views.DnsIpinfo)
router.register(r'getdnsinfobydnsip/(?P<dnsip>.*)',views.GetIdByDnsip,base_name = 'dnsip')
#对zone文件的管理
router.register(r'dnszone',views.Dnszoneinfo)
router.register(r'getidbyzone/(?P<zonename>.*)',views.GetIdByZone,base_name = 'zonename')
#对策略的管理
router.register(r'nameidpolicy',views.NameidPolciyinfo)
router.register(r'getidbypolicyname/(?P<policyname>.*)',views.GetIdByPolicy,base_name = 'policyname')
#对虚拟设备的管理
vip_router.register(r'vipdevice',views.VipDeviceinfo)
vip_router.register(r'getidbyvipname/(?P<vipname>.*)',views.GetIdByVipdev,base_name = 'vipname')
#依据节点id获取内容
vip_router.register(r'getidbynodename/(?P<nodename>.*)',views.GetIdByNodeName,base_name = 'nodename')

#对view的信息管理
router.register(r'viewtype',views.Viewtypeinfo)
router.register(r'view',views.Viewinfo)
router.register(r'getidbyfatherid/(?P<fatherid>[0-9]+)',views.GetIdByFatherid,base_name = 'viewid')
router.register(r'getidbyviewinfo/(?P<country>.*)/(?P<isp>.*)/(?P<region>.*)/(?P<province>.*)/(?P<city>.*)',views.GetIdByViewInfo,base_name = 'viewidinfo')
#对nameid的管理
router.register(r'nameid', views.Nameidinfo)

#对nameid view的管理
router.register(r'nameidview',views.NameidViewinfo)
#通过域名id和viewid获取对应的view信息
router.register(r'getidbynameview/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)',views.GetIdByNameidViewid,base_name = 'nameidview')
#通过域名id获取详细的view信息
router.register(r'getitembynameid/(?P<nameid>[0-9]+)',views.GetItemBynameid,base_name='nameidviewinner')


#对nameid view device的管理
router.register(r'nameidviewdevice',views.NameidViewDeviceinfo)
router.register(r'getdidbynameview/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)',views.GetDIdByNameidViewid,base_name = 'dnameidview')
#通过设备ip和nameid,viewid查找内容
router.register(r'nameidviewaddress/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)/(?P<ip>.*)',views.NameidViewAddress,base_name='nameidviewaddress')
#通过设备nodeid和nameid,viewid查找内容
router.register(r'nameidviewnodeid/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)/(?P<nodeid>.*)',views.NameidViewNodeid,base_name='nameidviewnode')
#通过nameid,viewid,deviceid获取记录
router.register(r'getidbynameviewdevice/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)/(?P<deviceid>[0-9]+)',views.GetIdByNameidViewidDeviceid,base_name = 'nameidviewiddeviceid')
#通过域名id获取name,device信息
router.register(r'getnamedevinfo/(?P<nameid>[0-9]+)',views.GetNameDevInfoByNameid,base_name='nameid')
#批量添加ip
#router.register(r'nameidviewMulip',views.NameidViewMulipinfo,base_name='iplist')

#对cname的管理
router.register(r'cname',views.CnameInfo)
router.register(r'getidbyopsubu/(?P<cname>.*)/(?P<operator>.*)/(?P<supplier>.*)/(?P<bussiness>.*)',views.GetItemByOpSuBu,base_name = 'opsubu')
#router.register(r'getidbycname/(?P<cname>.*)',views.GetIdByCname,base_name = 'cname')
#对nameid view cname的管理
router.register(r'nameidviewcname',views.NameidViewCnameinfo)
router.register(r'getcidbynameview/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)',views.GetCIdByNameidViewid,base_name = 'cnameidview')
#通过nameid.viewid,cnameid查找记录
router.register(r'getcidbynameviewcname/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)/(?P<cnameid>[0-9]+)',views.GetCIdByNameidViewidCnameid,base_name = 'nameidviewidcnameid')
#通过nameid,viewid,cname查找
router.register(r'nameidviewcname/(?P<nameid>[0-9]+)/(?P<viewid>[0-9]+)/(?P<cname>.*)',views.NameidViewCname,base_name='nameidviewcname')
#通过域名id获取view,cname信息
router.register(r'getnamecnameinfo/(?P<nameid>[0-9]+)',views.GetNameCnameInfoByNameid,base_name='nameidcname')


#对adminip的管理
router.register('adminip',views.AdminIpInfo)
router.register(r'getadminidbyviewinfo/(?P<isp>.*)/(?P<region>.*)/(?P<province>.*)',views.GetAdminIdByViewInfo,base_name = 'viewadminidinfo')
router.register(r'getadmininfobyadminnode/(?P<nodeid>.*)/(?P<adminip>.*)',views.GetIdByAdminResourse,base_name ='nodeadminip')
#对探测任务的管理
router.register('detecttask',views.DetectTaskInfo)
router.register(r'getidbytaskname/(?P<taskname>.*)',views.GetIdByTaskInfo,base_name='getidbytaskname')

#汇报数据可用性的接口
router.register('putdeviceavailability',views.DetectDeviceAvailabilityInfo,base_name='putdevice')
#展示数据的
router.register('showputdeviceavailability',views.ShowDetectDeviceAvailabilityInfo)

#对设备可用性探测数据有效性的控制
router.register('deviceavailabilitystandard',views.DetectDeviceAvailabilityStandardInfo)
router.register(r'getstandardinfo/(?P<standard>.*)',views.GetIdByStandardInfo,base_name='getstandardinfo')


urlpatterns = [
    path('gettask/',views.url_get_vipaddress_from_cache),
    path('getnameid/',views.url_get_nameid_from_cache),
    path('getzone/',views.url_get_zone_from_cache),
    path('getdnstype/',views.url_get_dnstype_from_cache),
    
    #获取经过策略以后的解析
    path('getqdnsnameidconfig/',views.url_get_nameidqdnsconfig),

    #删除nameid view关系表中的view的时候，需要同时删除该view在nameid view device表和nameid view cname关系表中的记录
    path('delnameidview/',views.NameidViewDelinfo),

    #给指定域名和view添加设备，级联父级设备，如果父级view没有创建则创建
    path('nameidviewdevice_father/',views.NameidViewListDeviceinfo),
     
    #通过设备nodeid添加记录
    path('nameidviewnodeid/',views.NameidViewNodeidinfo),
    #通过设备nodeid删除记录
    path('nameidviewnodeiddel/',views.NameidViewNodeidDelinfo),

    #批量添加ip,支持筛选的方式
    path('nameidviewdevice_mul_select/',views.NameidViewDeviceMulSelinfo),
    #批量添加ip,支持文本的方式
    path('nameidviewdevice_mul_load/',views.NameidViewDeviceMulLoadinfo),

    #批量工具的查询入库
    path('nameidviewmul/',views.NameidViewDeviceNodeMulSel),   
    path('nameidviewnodemul/',views.NameidViewNodeMulSel),    
    
    #批量工具批量替换ip
    path('nameidviewdevice_mul_replace/',views.NameidViewDeviceMulRepinfo),
    #批量工具批量添加ip
    path('nameidviewdevice_mul_append/',views.NameidViewDeviceMulAppendinfo),
    #批量工具批量删除ip
    path('nameidviewdevice_mul_del/',views.NameidViewDeviceMulDelinfo),
    
    #给指定域名和view添加cname，级联父级设备，如果父级view没有创建则创建
    path('nameidviewcname_father/',views.NameidViewListCnameinfo),
    
    #维护节点上下线
    path('maintainresource/',views.MaintainResource),
    #调整节点状态,是否采用探测数据
    path('adjutresourcestatus/',views.AdjustResourceStatus),
    #删除资源
    path('delresource/',views.DelResource),

    #修改探针的探测开关
    path('detetcswitch/',views.DetectSwitch),
    #删除探测，可以是节点或者ip维度
    path('deldetectresource/',views.DelDetectResource),

    path('', include(router.urls)),
    path('', include(vip_router.urls)),
]
from Polaris.init.gslb_init import scheduler
scheduler.start()
