from . import validators


def move(game, player, fila, columna):
    """
    Permite a un jugador realizar un movimiento en la partida,
    actualizando el estado del tablero y verificando si hay un ganador o
    un empate después de cada movimiento.

    Args:       game (Game): La instancia de la partida en la que se
                    realizará el movimiento.
                player (Player): El jugador que realiza el movimiento.
                fila (int): La fila donde se desea colocar la ficha (0-2).
                columna (int): La columna donde se desea colocar la ficha
                    (0-2).

    Returns:    dict: Un diccionario con estructura
                {"error": str, "data": dict}
                donde "error" es un mensaje de error si ocurrió alguno, o None
                si no hubo errores, y "data" contiene información relevante
                sobre el resultado del movimiento, como un mensaje de victoria
                o empate, o None si el juego continúa.
    """

    result = {"error": None, "data": None}

    if game.status != "ongoing":
        result["error"] = "El juego no está en progreso."
        return result

    if not validators.is_valid_player(player, game):
        result["error"] = "Jugador no forma parte de la partida."
        return result

    if not validators.is_valid_turn(player, game.current_turn):
        result["error"] = "No es tu turno."
        return result

    if not validators.is_valid_position(fila, columna, game.board_state):
        result["error"] = "Posición no válida."
        return result

    position = fila * 3 + columna
    # Actualizar el estado del tablero
    board = list(game.board_state)
    if game.current_turn == game.player1:
        board[position] = "X"
        game.current_turn = game.player2
    else:
        board[position] = "O"
        game.current_turn = game.player1

    game.board_state = "".join(board)
    game.moves = game.moves + f"{player.name}:{position};"

    # Verificar si hay un ganador
    winner_token = validators.check_winner(game.board_state)
    if winner_token:
        game.status = "player1_wins" if winner_token == "X" else "player2_wins"
        game.winner = game.player1 if winner_token == "X" else game.player2
        result["data"] = {"message": f"Jugador {game.winner.name} gana!"}

    elif validators.is_draw(game.board_state):
        game.status = "draw"
        result["data"] = {"message": "El juego ha terminado en empate."}

    return result
