import mongomock
import pytest
from unittest.mock import patch

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

@pytest.fixture(autouse=True)
def mock_get_coords():
    from backend.compute_tools import quartier_cordonnes
    with patch.object(quartier_cordonnes, "get_coords") as mock:
        # Retourne les coordonnées que tu as testées en local
        mock.side_effect = lambda address: {
            "Aeroport Bordeaux": (44.8292748, -0.7125609),
            "7 rue Réné Bonnac, Cenon": (44.8570121, -0.5306309)
        }.get(address, (0.0, 0.0))
        yield mock