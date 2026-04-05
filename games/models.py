from django.db import models
from players.models import Player


class Game(models.Model):
    """
    Modelo para representar una partida de Tic Tac Toe entre dos jugadores.
    """

    STATUS_CHOICES = {
        "waiting": "Esperando oponente",
        "ongoing": "En curso",
        "player1_wins": "Player 1 gana",
        "player2_wins": "Player 2 gana",
        "draw": "Empate",
    }

    player1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="games_as_player1",
        null=False,
        blank=True,
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="games_as_player2",
        null=True,
        blank=True,
    )
    board_state = models.CharField(
        max_length=9, default="-" * 9, null=False, blank=True
    )  # Representación del tablero como una cadena de 9 caracteres
    current_turn = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, blank=True
    )  # Jugador que tiene el turno actual
    status = models.CharField(
        max_length=20, default="waiting", choices=STATUS_CHOICES
    )  # Estado de la partida
    winner = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="games_won",
    )  # Jugador ganador de la partida, si hay uno
    moves = models.TextField(
        default="", blank=True
    )  # Registro de movimientos realizados en la partida

    def __str__(self):
        return f"{self.player1} vs {self.player2} - Status: {self.status}"
