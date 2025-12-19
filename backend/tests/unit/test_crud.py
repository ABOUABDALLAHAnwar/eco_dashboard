import pytest

from backend.database import database_crud


def test_create(client_accounts_collection):
    """

    Parameters
    ----------
    client_accounts_collection :

    Returns
    -------

    """
    collection_crud = database_crud.CollectionCrud(client_accounts_collection)
    user = {"email": "test@example.com", "hashed_password": "pass"}
    collection_crud.create(user)
    stored_user = client_accounts_collection.find_one(
        {"email": "test@example.com"})
    assert stored_user is not None
    assert stored_user["email"] == "test@example.com"


def test_read(client_accounts_collection):
    """

    Parameters
    ----------
    client_accounts_collection :

    Returns
    -------

    """
    collection_crud = database_crud.CollectionCrud(client_accounts_collection)
    user = {"email": "test@example.com", "hashed_password": "pass"}
    collection_crud.create(user)
    data = collection_crud.read("test@example.com")
    assert data["email"] == "test@example.com"


def test_create_exists(client_accounts_collection):
    """

    Parameters
    ----------
    client_accounts_collection :

    Returns
    -------

    """

    collection_crud = database_crud.CollectionCrud(client_accounts_collection)
    user = {"email": "test@example.com", "hashed_password": "pass"}

    collection_crud.create(user)

    # Si on essaye de créer le même user, on doit lever une erreur
    with pytest.raises(Exception):
        collection_crud.create(user)


def test_delete(client_accounts_collection):
    """

    Parameters
    ----------
    client_accounts_collection :

    Returns
    -------

    """
    collection_crud = database_crud.CollectionCrud(client_accounts_collection)
    user = {"email": "test2@example.com", "hashed_password": "pass"}
    collection_crud.create(user)
    collection_crud.delete("test2@example.com")
    stored_user = client_accounts_collection.find_one(
        {"email": "test2@example.com"})
    assert stored_user is None


def test_update(client_accounts_collection):
    """

    Parameters
    ----------
    client_accounts_collection :

    Returns
    -------

    """
    collection_crud = database_crud.CollectionCrud(client_accounts_collection)
    user = {"email": "test2@example.com", "hashed_password": "pass"}
    collection_crud.create(user)
    collection_crud.update(
        "test2@example.com",
        {"email": "test2@example.com", "hashed_password": "newpass"},
    )
    stored_user = client_accounts_collection.find_one(
        {"email": "test2@example.com"})

    assert stored_user is not None
    assert stored_user["email"] == "test2@example.com"
