from rest_framework import generics
from rest_framework import filters

from .serializers import GraphicSerializer
from .models import Graphic

class GraphicList(generics.ListCreateAPIView):
    queryset = Graphic.objects.all().order_by('date_created')
    serializer_class = GraphicSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']

class GraphicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Graphic.objects.all().order_by('date_created')
    serializer_class = GraphicSerializer