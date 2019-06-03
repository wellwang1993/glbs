from Polaris.models import tb_fact_device_info
from Polaris.serializers import VipDeviceSerializer
#支持增删查改设备
class VipDeviceinfo(viewsets.ModelViewSet):
    queryset = tb_fact_device_info.objects.all()
    serializer_class = VipDeviceSerializer
