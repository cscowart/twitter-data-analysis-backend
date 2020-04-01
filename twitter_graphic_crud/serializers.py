from rest_framework.serializers import ModelSerializer
from .models import Graphic

class GraphicSerializer(ModelSerializer):
    class Meta:
        model = Graphic
        fields = ('id', 'author', 'date_created', 'graph_code_js')