from rest_framework import viewsets
from .models import InvoiceHeader
from .serializers import InvoiceHeaderSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = InvoiceHeader.objects.all()
    serializer_class = InvoiceHeaderSerializer
