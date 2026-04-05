from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from players.models import Player


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Login correcto"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
def register_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Nombre de usuario y contraseña son requeridos."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Creamos el usuario y el jugador asociado
    User.objects.create_user(username=username, password=password)
    Player.objects.create(user=User.objects.get(username=username), name=username)

    return Response({"message": "Registro exitoso"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout correcto"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_current_user(request):
    # Verificamos si el usuario está autenticado
    if request.user.is_authenticated:
        return Response({"username": request.user.username}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED
        )
