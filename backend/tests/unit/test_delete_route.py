# backend/tests/integration/test_signup.py
from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.database import collections_handeler
from backend.main import app
from backend.scripts import variables
from backend.users_handler import handle_users

# ---- Fixtures existantes ----
# mockdb, client_accounts_collection, client_actions_collection, user_profile_infos_collection


@pytest.fixture(autouse=True)
def mock_client_collection_methods(monkeypatch, client_accounts_collection):
    monkeypatch.setattr(
        collections_handeler.ClientCollection,
        "read",
        lambda self, email: client_accounts_collection.find_one({"email": email}),
    )
    monkeypatch.setattr(
        collections_handeler.ClientCollection,
        "delete",
        lambda self, email: client_accounts_collection.delete_one({"email": email}),
    )


@pytest.fixture(autouse=True)
def mock_all_collections(monkeypatch, client_accounts_collection):
    class MockClientCollection:
        def read(self, email):
            return client_accounts_collection.find_one({"email": email})

        def delete(self, email):
            client_accounts_collection.delete_one({"email": email})

    monkeypatch.setattr(collections_handeler, "ClientCollection", MockClientCollection)

    monkeypatch.setattr(
        collections_handeler,
        "UserProfileInfos",
        lambda: MagicMock(read=lambda x: None, delete=lambda x: None),
    )

    monkeypatch.setattr(
        collections_handeler,
        "ClientActions",
        lambda: MagicMock(read=lambda x: None, delete=lambda x: None),
    )


@pytest.fixture(autouse=True)
def mock_hash(monkeypatch):
    # Mock du hash password pour ne pas calculer réellement
    monkeypatch.setattr(handle_users, "hash_password", lambda x: f"hashed-{x}")


client = TestClient(app)


def test_delete_user(
    client_accounts_collection, user_profile_infos_collection, client_actions_collection
):
    # Créer un utilisateur dans le mock
    client_accounts_collection.insert_one(
        {"email": "test@test.com", "hashed_password": "pass"}
    )

    # Appel de la route DELETE
    # response = client.delete("/delete_account")
    response = client.delete("/delete_account?email=test@test.com")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert client_accounts_collection.find_one({"email": "test@test.com"}) is None
