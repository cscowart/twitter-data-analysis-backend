from rest_framework.views import APIView
from rest_framework.response import Response
from .twitter_api.twitter_api_calls import AuthinticatedAPI

# Create your views here.
# class LocationView(APIView):
#     """
#     Takes in a location and return tweets in the area
#     """
#     def get(self, request, format=None):
#         return


class HandleView(APIView):
    """
    Takes in a twitter handle and makes the query to return recent tweets made by the account
    """
    def get(self, request, handle, format=None):
        api = AuthinticatedAPI()
        # validate the handle data consists of only primitive types
        handle_data = api.get_handle_data(handle)
        return Response(handle_data)

class HandleValidateView(APIView):
    """
    Takes in a handle from the link and returns a user profile for validation
    """
    def get(self, request, handle, format=None):
        api = AuthinticatedAPI()
        user_data = api.get_user_data(handle)
        return Response(user_data)

class BotScoreView(APIView):
    """
    Takes in a handle from the link and returns a user profile for validation
    """
    def get(self, request, handle, format=None):
        api = AuthinticatedAPI()
        user_data = api.get_user_bot_score(handle)
        return Response(user_data)

# class TopicView(APIView):
#     """
#     Takes in a trending topic and makes the query to return tweets including the topic
#     """
#     def get(self, request, format=None):
#         return