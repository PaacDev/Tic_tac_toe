def is_valid_turn(player, current_turn):
    """
    Valida si es el turno del jugador.
    Args:       player (Player): El jugador que intenta hacer un movimiento.
                current_turn (Player): El jugador que tiene el turno
                    actual.

    Returns:        bool: True si es el turno del jugador, False de lo
        contrario.
    """

    return player == current_turn


def is_valid_position(row, column, board):
    """
    Valida la posición en el tablero.
    Args:       row (int): La fila de la posición.
                column (int): La columna de la posición.
                board (str): El estado actual del tablero representado
                como una cadena de 9 caracteres.

    Returns:        bool: True si la posición es válida, False de lo
        contrario.
    """

    # Comprobamos que la posición esté dentro de los límites del tablero
    if row < 0 or row > 2 or column < 0 or column > 2:
        return False
    # Comprobamos que la celda no esté ocupada
    if board[row * 3 + column] != "-":
        return False
    return True


def check_winner(board):
    """
    Verifica si hay un ganador en el tablero.
    Args:       board (str): El estado actual del tablero representado
                como una cadena de 9 caracteres.

    Returns:        str: Token del jugador ganador ('X' o 'O') o None si
        no hay ganador.
    """

    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],  # Filas
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],  # Columnas
        [0, 4, 8],
        [2, 4, 6],  # Diagonales
    ]

    for combination in winning_combinations:
        if (
            board[combination[0]]
            == board[combination[1]]
            == board[combination[2]]
            != "-"
        ):
            return board[combination[0]]

    return None


def is_draw(board):
    """
    Verifica si el juego ha terminado en empate.
    Args:       board (str): El estado actual del tablero representado
                como una cadena de 9 caracteres.

    Returns:        bool: True si el juego es un empate, False de lo
        contrario.
    """

    return "-" not in board


def is_valid_player(player, game):
    """
    Valida si el jugador es parte del juego.
    Args:       player (Player): El jugador a validar.
                game (Game): El juego en el que se está validando el
                jugador.

    Returns:        bool: True si el jugador es parte del juego, False
        de lo contrario.
    """

    return player == game.player1 or player == game.player2
