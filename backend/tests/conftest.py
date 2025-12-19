import mongomock
import pytest

@pytest.fixture
def mockdb():
    client = mongomock.MongoClient()
    mockdb = client["app_eco_part"]
    return mockdb

@pytest.fixture
def client_accounts_collection(mockdb):
    # Crée une "fake" MongoDB en mémoire

    client_accounts_collection = mockdb["client_accounts"]
    return client_accounts_collection

@pytest.fixture
def client_actions_collection(mockdb):
    # Crée une "fake" MongoDB en mémoire

    client_actions_collection = mockdb["client_actions"]
    return client_actions_collection


@pytest.fixture
def user_profile_infos_collection(mockdb):
    # Crée une "fake" MongoDB en mémoire

    user_profile_infos_collection = mockdb["user_profile"]
    return user_profile_infos_collection

