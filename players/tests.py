from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Player


class PlayerTests(TestCase):
    def test_player_creation(self):
        """Test para verificar que se puede crear un jugador correctamente."""

        user = User.objects.create_user(username="testuser", password="testpass")
        player = Player.objects.create(user=user, name="Test Player")

        self.assertEqual(player.user, user)
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(str(player), "Test Player")

    def test_player_str(self):
        """Test para verificar que el método __str__ del modelo Player devuelve el nombre del jugador."""

        user = User.objects.create_user(username="testuser", password="testpass")
        player = Player.objects.create(user=user, name="Test Player")

        self.assertEqual(str(player), "Test Player")

    def test_create_player_user_login(self):
        """Test para verificar que se puede crear un jugador a partir de un usuario autenticado."""

        user1 = User.objects.create_user(username="testuser", password="testpass")

        client = APIClient()
        client.force_authenticate(user=user1)

        response = client.post("/api/players/", {"name": "testuser"})
        self.assertEqual(response.status_code, 201)
        player = Player.objects.first()
        self.assertEqual(player.user, user1)
        self.assertEqual(player.name, user1.username)
