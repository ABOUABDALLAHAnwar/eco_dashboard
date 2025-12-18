import mongomock
import pytest

@pytest.fixture
def client_accounts_collection():
    # Crée une "fake" MongoDB en mémoire
    client = mongomock.MongoClient()
    db = client["app_eco_part"]
    client_accounts_collection = db["client_accounts"]

    return client_accounts_collection