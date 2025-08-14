from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



# @api_view(['POST'])
# def register(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#
#     if not username or not password:
#         return Response({"error": "Mising username or password field"}, status=status.HTTP_400_BAD_REQUEST)
#     if User.objects.filter(username=username).exists():
#         return Response({"error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)
#     user = User.objects.create_user(username=username, password=password)
#     return Response({"message": "User Registered"}, status=status.HTTP_201_CREATED)
