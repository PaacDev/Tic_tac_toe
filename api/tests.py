from django.test import TestCase
from rest_framework.test import APIClient

class APICoreTests(TestCase):
    def test_register_user(self):
        # Test registro de usuario
        response = self.client.post(
            "/register/", {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.data)
        self.assertIn("Registro exitoso", response.data["message"])

    def test_register_user_missing_fields(self):
        # Test registro con campos faltantes
        response = self.client.post("/register/", {"username": "testuser"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertIn(
            "Nombre de usuario y contraseña son requeridos.", response.data["error"]
        )

        response = self.client.post("/register/", {"password": "testpass"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertIn(
            "Nombre de usuario y contraseña son requeridos.", response.data["error"]
        )

    def test_login_user(self):
        # Test login de usuario
        self.client.post("/register/", {"username": "testuser", "password": "testpass"})
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)
        self.assertIn("Login correcto", response.data["message"])

    def test_login_user_invalid_credentials(self):
        # Test login con credenciales inválidas
        response = self.client.post(
            "/login/", {"username": "nonexistent", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.data)
        self.assertIn("Credenciales inválidas", response.data["error"])

    def test_logout_user(self):
        # Test logout de usuario
        self.client.post("/register/", {"username": "testuser", "password": "testpass"})
        self.client.post("/login/", {"username": "testuser", "password": "testpass"})
        response = self.client.post("/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)
        self.assertIn("Logout correcto", response.data["message"])

    def test_get_current_user(self):
        # Test obtener usuario actual
        self.client = APIClient()
        self.client.post("/register/", {"username": "testuser", "password": "testpass"})
        self.token = self.client.post(
            "/api/token/", {"username": "testuser", "password": "testpass"}
        ).data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get("/current_user/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], "testuser")


    def test_get_current_user_unauthenticated(self):
        # Test obtener usuario actual sin autenticación
        # Reiniciamos el cliente para eliminar credenciales
        response = self.client.get("/current_user/")
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.data)
        self.assertIn("Usuario no autenticado", response.data["error"])
