from rest_framework import generics

from .serializers import GraphicSerializer
from .models import Graphic

class GraphicList(generics.ListCreateAPIView):
    queryset = Graphic.objects.all().order_by('date_created')
    serializer_class = GraphicSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = Graphic.objects.all()
        title = self.request.query_params.get('search', None)
        if title is not None:
            queryset = queryset.filter(title__ilike=title)
        return queryset

class GraphicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Graphic.objects.all().order_by('date_created')
    serializer_class = GraphicSerializer