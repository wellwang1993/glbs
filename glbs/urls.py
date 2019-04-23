from django.urls import path,include
from glbs import views

from glbs.views import Nameidhh
snippet_detail = Nameidhh.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_list = Nameidhh.as_view({
    'get': 'list',
    'post': 'create'
})

'''
urlpatterns = [
    path('dnszone/', views.DnszoneList.as_view()),
    path('dnstype/', views.DnstypeList.as_view()),
    
    path('nameid/', snippet_list),
    path('nameidpolicy/', views.NameidPolciyList.as_view()),
    path('nameiddetail/<int:pk>/',snippet_detail),
    
]
'''
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'dnstype',views.Dnstypeinfo)
router.register(r'getidbydnsname/(?P<dnsname>.*)',views.GetIdByDnsname,base_name = 'dnsname')

router.register(r'dnszone',views.Dnszoneinfo)
router.register(r'getidbyzone/(?P<zonename>.*)',views.GetIdByZone,base_name = 'zonename')

router.register(r'nameidpolicy',views.NameidPolciyinfo)
router.register(r'getidbypolicyname/(?P<policyname>.*)',views.GetIdByPolicy,base_name = 'policyname')

router.register(r'vipdevice',views.VipDeviceinfo)
router.register(r'getidbyvipname/(?P<vipname>.*)',views.GetIdByVipdev,base_name = 'vipname')

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
router.register(r'del',views.DelByNameid)

router.register(r'nameidviewdevice',views.NameidViewDeviceinfo)
router.register(r'getdidbynameview/(?P<nameid>.*)/(?P<viewid>.*)',views.GetDIdByNameidViewid,base_name = 'dnameidview')


urlpatterns = [
   # path('ajax/GetRegion',views.GetRegion, name='ajax_GetRegion'),
    path('', include(router.urls)),
]
