# Tic Tac Toe API (Django)

API REST para gestionar partidas de **Tic Tac Toe** entre usuarios.

---

## Requisitos

- Python 3.x
- pip
- (Opcional) entorno virtual `venv`

---

## Instalación

### 1) Clonar el repositorio

```bash
git clone https://github.com/PaacDev/Tic_tac_toe.git
cd Tic_tac_toe
```

### 2) Crear entorno virtual

```bash
python -m venv venv
```

### 3) Activar entorno virtual

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 4) Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Puesta en marcha

### 1) Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2) Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 3) Ejecutar servidor

```bash
python manage.py runserver
```

### 4) Probar endpoints

Puedes usar herramientas como Postman o cURL para probar los 
endpoints descritos a continuación.

La mayoría de endpoints requieren usuario autenticado.

---

## Registro y Autenticación

### Registro

`POST /register/`

**Request**

```json
{
  "username": "juan",
  "password": "12345"
}
```

**Response**

```json
{
  "message": "Registro exitoso",
}
```

### Login

Se ha implementado un login de sesión tradicional para facilitar pruebas con el navegador. Para autenticación basada en tokens JWT, se pueden usar los endpoints de `rest_framework_simplejwt`:

Login JWT: `POST /api/token/`
**Request**

```json
{
  "username": "juan",
  "password": "12345"
}
```

**Response**

```json
{
  "refresh": "TOKEN_REFRESH",
  "access": "TOKEN_ACCESS"
}
```

Refresh JWT: `POST /api/token/refresh/`

**Response**

```json
{
  "access": "NEW_TOKEN_ACCESS"
}
```

Login tradicional de sesión: `POST /login/`

**Request**

```json
{
  "username": "juan",
  "password": "12345"
}
```

**Response**

```json
{
  "message": "Login correcto",
}
```

---

## Endpoints de juego

### Crear partida

`POST /api/games/new_game/`

**Request**

```json
{}
```

**Response**

```json
{
  "id": 1,
  "player1_name": "juan",
  "status": "waiting"
}
```

---

### Listar partidas que esperan oponente

`GET /api/games/waiting_games/`

**Response**

```json
[
  { "id": 1, "player1_name": "juan" },
  { "id": 2, "player1_name": "maria" }
]
```

### Unirse a una partida

`POST /api/games/{id}/join_game/`

**Request**

```json
{}
```

**Response**

```json
{
  "id": 1,
  "player1_name": "juan",
  "player2_name": "maria",
  "status": "ongoing"
}
```
### Turno inicial

Asignar el turno inicial a un jugador.

El jugador que realiza la solicitud a este endpoint tendrá el primer turno.

`POST /api/games/{id}/set_current_turn/`

**Request**

```json
{}
```

**Response**

```json
{
    "current_turn_name": "juan"
}
```


### Hacer un movimiento

`POST /api/games/{id}/make_move/`

La representación del tablero es una matriz 3x3

**Request**

```json
{
  "fila": 0,
  "columna": 2
}
```

**Response**

```json
{
  "board_matrix": [["X", "-", "O"], ["-", "-", "-"], ["-", "-", "-"]]
}
```

La  interpretación de la matriz es la siguiente:
- "X" representa las casillas ocupadas por el jugador 1.
- "O" representa las casillas ocupadas por el jugador 2.
- "-" representa las casillas vacías.

- La primera lista corresponde a la fila 0, la segunda a la fila 1 y la tercera a la fila 2.
- Dentro de cada lista, el primer elemento corresponde a la columna 0, el segundo a la columna 1 y el tercero a la columna 2.

---

### Listar partidas ganadas por un jugador

`GET /api/games/win_games/`

**Response**

```json
[
  { "id": 1, "player1_name": "juan", "player2_name": "maria" },
  { "id": 2, "player1_name": "maria", "player2_name": "juan" }
]
```

### Listar partidas jugadas por un jugador

`GET /api/games/my_games/`

**Response**

```json
[
  { "id": 1, "player1_name": "juan", "player2_name": "maria", "status": "ongoing", "moves": "" },
  { "id": 2, "player1_name": "maria", "player2_name": "juan", "status": "ongoing", "moves": "" }
]

```
### Log de movimientos

El campo "moves" es una cadena con el formato: nombre_jugador: (fila, columna); ... representando la secuencia de movimientos realizados en la partida.
Ejemplo: "juan: (0, 0); maria: (1, 1); juan: (0, 1); maria: (2, 2); juan: (0, 2);"
