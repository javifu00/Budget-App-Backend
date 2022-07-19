from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {
            "Endpoint": "/transactions",
            "method": "GET",
            "body": {"body": ""},
            "description": "Returns an array of the users transactions",
        },
        {
            "Endpoint": "/transactions/id",
            "method": "GET",
            "body": None,
            "description": "Returns a single transaction object",
        },
        {
            "Endpoint": "/transactions/create/",
            "method": "POST",
            "body": {"body": ""},
            "description": "Creates new transaction with data sent in post request",
        },
        {
            "Endpoint": "/transactions/id/update/",
            "method": "PUT",
            "body": {"body": ""},
            "description": "Edits an existing transaction with data sent in post request",
        },
        {
            "Endpoint": "/transactions/id/delete/",
            "method": "DELETE",
            "body": None,
            "description": "Deletes an exiting transaction",
        },
        {
            "Endpoint": "/goals/",
            "method": "GET",
            "body": None,
            "description": "Returns an array of the users goals",
        },
        {
            "Endpoint": "/goals/id",
            "method": "GET",
            "body": None,
            "description": "Returns a single goal object",
        },
        {
            "Endpoint": "/goals/create/",
            "method": "POST",
            "body": {"body": ""},
            "description": "Creates new goal with data sent in post request",
        },
        {
            "Endpoint": "/goals/id/update/",
            "method": "PUT",
            "body": {"body": ""},
            "description": "Edits an existing goal with data sent in post request",
        },
        {
            "Endpoint": "/goals/id/delete/",
            "method": "DELETE",
            "body": None,
            "description": "Deletes and exiting goal",
        },
    ]
    return Response(routes)
