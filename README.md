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

- Partidas: <http://127.0.0.1:8000/api/games/>
- Jugadores: <http://127.0.0.1:8000/api/players/>
- Login DRF (navegable): <http://127.0.0.1:8000/api-auth/login/>

---

## Autenticación

La mayoría de endpoints requieren usuario autenticado.

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

`POST /login/`

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
  "player1": "juan",
  "status": "waiting"
}
```

---

### Listar partidas esperando oponente

`GET /api/games/waiting_games/`

**Response**

```json
[
  { "id": "id", "player1": "id" },
  { "id": "id", "player1": "id" }
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
  "player1": "juan",
  "player2": "maria",
  "status": "ongoing"
}
```
### Turno inicial

El jugador que realiza la solicitud a este endpoint tendrá el primer turno.

`POST /api/games/{id}/set_current_turn/`

**Request**

```json
{}
```

**Response**

```json
{
    "current_turn": "id"
}
```


### Hacer un movimiento

`POST /api/games/{id}/make_move/`

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

---

### Listar partidas ganadas por un jugador

`GET /api/games/win_games/`

**Response**

```json
[
  { "id": "id", "player1": "id", "player2": "id" },
  { "id": "id", "player1": "id", "player2": "id" }
]
```

### Listar partidas jugadas por un jugador

`GET /api/games/my_games/`

**Response**

```json
[
  { "id": "id", "player1": "id", "player2": "id", "status": "ongoing", "moves": "" },
  { "id": "id", "player1": "id", "player2": "id", "status": "ongoing", "moves": "" }
]

```
