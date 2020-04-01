from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # # view data by location 
    # path('location', views.LocationView.as_view()),
    # view data by users 
    path('handle_data/<handle>', views.HandleView.as_view()),
    # user bot score
    path('handle_bot_score/<handle>', views.BotScoreView.as_view()),
    # validate user
    path('validate_handle/<handle>', views.HandleValidateView.as_view())
    # # view data by topic
    # path('topic', views.TopicView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)