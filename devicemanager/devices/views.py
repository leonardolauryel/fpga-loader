from rest_framework import viewsets
from .models import FPGA
from .serializers import FPGASerializer

class FPGAViewSet(viewsets.ModelViewSet):
    queryset = FPGA.objects.all()
    serializer_class = FPGASerializer

    def get_queryset(self):
        queryset = FPGA.objects.all()
        serial_number = self.request.query_params.get('serial_number', None)
        name = self.request.query_params.get('name', None)

        if serial_number is not None:
            queryset = queryset.filter(serial_number__exact=serial_number)

        if name is not None:
            queryset = queryset.filter(name__exact=name)

        return queryset