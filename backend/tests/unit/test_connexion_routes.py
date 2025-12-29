# backend/tests/integration/test_signup.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.main import app
from backend.scripts import variables
from backend.users_handler import handle_users
from backend.database import collections_handeler


# ---- Fixtures existantes ----
# mockdb, client_accounts_collection, client_actions_collection, user_profile_infos_collection

@pytest.fixture(autouse=True)
def mock_client_collection(monkeypatch, client_accounts_collection):
    # Remplace la collection réelle par le mock
    monkeypatch.setattr(variables, "client_accounts_collection", client_accounts_collection)

    # Remplace la méthode add_new_user pour ne rien écrire réellement
    monkeypatch.setattr(collections_handeler.ClientCollection, "add_new_user", MagicMock())


@pytest.fixture(autouse=True)
def mock_hash(monkeypatch):
    # Mock du hash password pour ne pas calculer réellement
    monkeypatch.setattr(handle_users, "hash_password", lambda x: f"hashed-{x}")


client = TestClient(app)


# ---- Tests ----
def test_signup_success(client_accounts_collection):
    data = {"email": "test@test.com", "password": "123456"}

    # s'assurer que l'email n'existe pas encore
    assert client_accounts_collection.find_one({"email": data["email"]}) is None

    response = client.post("/signup", data=data)

    assert response.status_code == 201
    json_data = response.json()
    assert json_data["message"] == "User created successfully"
    assert json_data["email"] == data["email"]


def test_signup_existing_email(client_accounts_collection):
    # Ajouter un email existant dans la collection mock
    client_accounts_collection.insert_one({"email": "existing@test.com"})

    response = client.post("/signup", data={"email": "existing@test.com", "password": "123456"})

    assert response.status_code == 400
    json_data = response.json()
    assert json_data["detail"] == "Email already exists."


def test_login_success(monkeypatch):
    # Mock de la méthode read pour qu'elle retourne un utilisateur simulé
    mock_user = {"email": "test@test.com", "hashed_password": "hashed-123456"}
    def mock_read(self, username):
        if username == mock_user["email"]:
            return mock_user
        return None

    monkeypatch.setattr(
        collections_handeler.ClientCollection,
        "read",
        mock_read
    )

    # Mock de verify_password
    monkeypatch.setattr(handle_users, "verify_password", lambda pw, hashed: hashed == f"hashed-{pw}")

    # Test login
    response = client.post(
        "/login",
        data={"username": "test@test.com", "password": "123456"}
    )


    assert response.status_code == 200
    assert "access_token" in response.json()



