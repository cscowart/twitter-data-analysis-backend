from rest_framework import generics

from .serializers import GraphicSerializer
from .models import Graphic

class GraphicList(generics.ListCreateAPIView):
    queryset = Graphic.objects.all().order_by('date_created')
    serializer_class = GraphicSerializer

class GraphicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Graphic.objects.all().order_by('date_created')
    serializer_class = GraphicSerializer