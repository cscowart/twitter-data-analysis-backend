from django.urls import include, path


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('graphics/', include('twitter_graphic_crud.urls')), 
    path('api/', include('twitter_data_processing.urls')), 
]
