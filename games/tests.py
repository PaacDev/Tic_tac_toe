from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from games.models import Game
from players.models import Player


class GameTests(TestCase):
    def setUp(self):
        """
        Configura el entorno de prueba creando dos jugadores y un
        usuario para cada uno.
        """

        self.user1 = User.objects.create_user(
            username="testuser1", password="testpass"
        )
        self.player1 = Player.objects.create(
            user=self.user1, name=self.user1.username
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpass"
        )
        self.player2 = Player.objects.create(
            user=self.user2, name=self.user2.username
        )

    def test_new_game(self):
        """Test para verificar que se puede crear una
        nueva partida correctamente."""

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post("/api/games/new_game/")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.first()
        self.assertEqual(game.player1, self.player1)
        self.assertEqual(game.status, "waiting")

    def test_join_game(self):
        """Test para verificar que un jugador puede
        unirse a una partida correctamente."""

        game = Game.objects.create(player1=self.player1)

        client = APIClient()
        client.force_authenticate(user=self.user2)

        response = client.post(f"/api/games/{game.id}/join_game/")
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.player2, self.player2)
        self.assertEqual(game.status, "ongoing")

    def test_join_game_invalid_player(self):
        """Test para verificar que un jugador no puede
        unirse a una partida si ya es parte de ella, si
        intenta unirse a su propia partida o si la partida
        ya tiene dos jugadores y anonimos.
        """

        game = Game.objects.create(player1=self.player1)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        # Intentar unirse a su propia partida
        response = client.post(f"/api/games/{game.id}/join_game/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

        # Crear una partida con ambos jugadores
        game.player2 = self.player2
        game.status = "ongoing"
        game.save()

        # Intentar unirse a una partida que ya tiene dos jugadores
        response = client.post(f"/api/games/{game.id}/join_game/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

        # Tercer jugador intenta unirse a una partida con dos jugadores
        user3 = User.objects.create_user(
            username="testuser3", password="testpass"
        )
        Player.objects.create(user=user3, name=user3.username)
        client.force_authenticate(user=user3)
        response = client.post(f"/api/games/{game.id}/join_game/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        # Anonimo intenta unirse a una partida con dos jugadores
        client.force_authenticate(user=None)
        response = client.post(f"/api/games/{game.id}/join_game/")
        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_waiting_games(self):
        """Test para verificar que se pueden listar
        las partidas que están esperando un oponente."""

        Game.objects.create(player1=self.player1)
        Game.objects.create(
            player1=self.player2, player2=self.player1, status="ongoing"
        )

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get("/api/games/waiting_games/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["player1"], self.player1.id)

    def test_set_current_turn(self):
        """Test para verificar que se puede asignar
        el primer turno a un jugador al iniciar la
        partida."""

        game = Game.objects.create(
            player1=self.player1, player2=self.player2, status="ongoing"
        )

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(f"/api/games/{game.id}/set_current_turn/")
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.current_turn, self.player1)

        # Intentar asignar el turno nuevamente
        response = client.post(f"/api/games/{game.id}/set_current_turn/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        # Turno asignado por jugador no parte de la partida
        user3 = User.objects.create_user(
            username="testuser3", password="testpass"
        )
        Player.objects.create(user=user3, name=user3.username)
        client.force_authenticate(user=user3)
        response = client.post(f"/api/games/{game.id}/set_current_turn/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertIn(
            response.data["error"],
            [
                "Jugador no forma parte de la partida"
            ],
        )

    def test_win_games(self):
        """Test para verificar que se puede obtener
        la lista de partidas ganadas por un jugador."""

        Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="player1_wins",
            winner=self.player1,
        )
        Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="player2_wins",
            winner=self.player2,
        )
        Game.objects.create(player1=self.player1, status="waiting")

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get("/api/games/win_games/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_my_games(self):
        """Test para verificar que se puede obtener
        la lista de partidas en las que el jugador actual
        es player1 o player2."""

        Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="player1_wins",
            winner=self.player1,
        )
        Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="player2_wins",
            winner=self.player2,
        )
        Game.objects.create(player1=self.player1, status="waiting")
        Game.objects.create(player1=self.player2, status="waiting")

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get("/api/games/my_games/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_make_move(self):
        """Test para verificar que un jugador puede
        realizar un movimiento en la partida y que el
        estado del tablero se actualiza correctamente."""

        game = Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="ongoing",
            current_turn=self.player1,
        )

        client = APIClient()
        client.force_authenticate(user=self.user1)

        move_data = {"fila": 0, "columna": 0}
        response = client.post(
            f"/api/games/{game.id}/make_move/", move_data
        )
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.board_state[0], "X")
        self.assertEqual(game.current_turn, self.player2)
        # Intentar hacer un movimiento fuera de turno
        response = client.post(
            f"/api/games/{game.id}/make_move/",
            {"fila": 0, "columna": 1},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

        # Intentar hacer un movimiento en una posición no válida
        client.force_authenticate(user=self.user2)
        response = client.post(
            f"/api/games/{game.id}/make_move/",
            {"fila": 0, "columna": 0},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        # Comprobar movimiento válido player2
        response = client.post(
            f"/api/games/{game.id}/make_move/",
            {"fila": 0, "columna": 1},
        )
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.board_state[1], "O")
        self.assertEqual(game.current_turn, self.player1)

    def test_make_move_invalid_game_status(self):
        """Test para verificar que no se pueden realizar
        movimientos en una partida que no está en curso."""

        game = Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="waiting",
            current_turn=self.player1,
        )

        client = APIClient()
        client.force_authenticate(user=self.user1)

        move_data = {"fila": 0, "columna": 0}
        response = client.post(
            f"/api/games/{game.id}/make_move/", move_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_make_move_win(self):
        """Test para verificar que el sistema detecta
        correctamente cuando un jugador gana la partida."""

        game = Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="ongoing",
            current_turn=self.player1,
            board_state="XX-OXO---",
        )

        client = APIClient()
        client.force_authenticate(user=self.user1)

        move_data = {"fila": 0, "columna": 2}
        response = client.post(
            f"/api/games/{game.id}/make_move/", move_data
        )
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.status, "player1_wins")
        self.assertEqual(game.winner, self.player1)

    def test_make_move_draw(self):
        """Test para verificar que el sistema detecta
        correctamente cuando la partida termina en empate."""

        game = Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="ongoing",
            current_turn=self.player1,
            board_state="-OXOXOOXO",
        )

        client = APIClient()
        client.force_authenticate(user=self.user1)

        move_data = {"fila": 0, "columna": 0}
        response = client.post(
            f"/api/games/{game.id}/make_move/", move_data
        )
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.status, "draw")

    def test_limit_positions(self):
        """Test para verificar que el sistema no
        permite realizar movimientos en posiciones fuera
        del tablero."""

        game = Game.objects.create(
            player1=self.player1,
            player2=self.player2,
            status="ongoing",
            current_turn=self.player1,
        )

        client = APIClient()
        client.force_authenticate(user=self.user1)

        # Intentar hacer un movimiento fuera del tablero
        response = client.post(
            f"/api/games/{game.id}/make_move/",
            {"fila": 3, "columna": 0},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

        response = client.post(
            f"/api/games/{game.id}/make_move/",
            {"fila": 0, "columna": 3},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
