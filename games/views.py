from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Game
from .serializers import GameSerializer
from .services import validators, game_logic


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para manejar las operaciones CRUD y acciones
    personalizadas relacionadas con el modelo Game."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def new_game(self, request):
        """Crea una nueva partida y devuelve su información básica."""

        player1 = request.user.player
        game = Game.objects.create(player1=player1)
        # Solo incluimos los campos necesarios para mostrar
        # la información básica de la partida recién creada
        serializer = self.get_serializer(
            game, fields=("id", "player1", "status")
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def waiting_games(self, request):
        """Devuelve partidas esperando oponente."""

        waiting_games = Game.objects.filter(status="waiting")
        # Solo incluimos los campos necesarios para mostrar la lista
        # de partidas esperando oponente
        serializer = self.get_serializer(
            waiting_games, many=True, fields=("id", "player1")
        )

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def join_game(self, request, pk=None):
        """Permite unirse a una partida esperando oponente."""

        game = self.get_object()
        if game.status != "waiting":
            return Response(
                {"error": "Partida no disponible para unirse."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        player2 = request.user.player
        # Validamos que jugador no sea player1 y no esté en la partida
        if validators.is_valid_player(player2, game):
            return Response(
                {"error": "El jugador ya está en el juego."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Actualizamos la partida con nuevo jugador y estado 'ongoing'
        game.player2 = player2
        game.status = "ongoing"
        game.save()
        # Información de la partida a la que se unió
        serializer = self.get_serializer(
            game, fields=("id", "player1", "player2", "status")
        )
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def set_current_turn(self, request, pk=None):
        """Asigna turno inicial. Solo una vez por partida."""

        game = self.get_object()

        # Verificar que jugador es parte de partida y turno sin asignar
        if not validators.is_valid_player(
            request.user.player, game
        ):
            return Response(
                {"error": "Jugador no forma parte de la partida"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if game.current_turn is not None:
            return Response(
                {"error": "El turno ya ha sido establecido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Asignamos turno al jugador y actualizamos la partida
        game.current_turn = request.user.player
        game.save()
        # Campo del turno actual para mostrar quién juega
        serializer = self.get_serializer(game, fields=("current_turn",))
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def win_games(self, request):
        """Devuelve partidas ganadas por el jugador."""

        player = request.user.player
        won_games = Game.objects.filter(winner=player)
        serializer = self.get_serializer(
            won_games, many=True, fields=("id", "player1", "player2")
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def my_games(self, request):
        """Devuelve partidas del jugador como player1 o player2."""

        player = request.user.player
        my_games = (
            Game.objects.filter(player1=player)
            | Game.objects.filter(player2=player)
        )
        serializer = self.get_serializer(
            my_games,
            many=True,
            fields=(
                "id", "player1", "player2", "status", "moves"
            ),
        )
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def make_move(self, request, pk=None):

        game = self.get_object()

        result = game_logic.move(
            game, request.user.player, int(request.data.get("fila")),
            int(request.data.get("columna"))
        )

        if result["error"]:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if result["data"]:
            # Guardamos cambios antes de devolver resultado
            game.save()
            return Response(result["data"])

        # Guardamos cambios después del movimiento
        game.save()
        serializer = self.get_serializer(game, fields=("board_matrix",))
        return Response(serializer.data)
