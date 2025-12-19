def test_create_user_exists(mock_db):
    crud = CollectionCrud(mock_db)
    user = {"email": "test@example.com", "name": "Test"}

    crud.create(user)

    # Si on essaye de créer le même user, on doit lever une erreur
    with pytest.raises(Exception):
        crud.create(user)


def test_delete_user(mock_db):
    crud = CollectionCrud(mock_db)
    user = {"email": "test@example.com", "name": "Test"}
    crud.create(user)

    # Supprime le user
    crud.delete("test@example.com")

    # Vérifie que la collection est vide
    assert mock_db.find_one({"email": "test@example.com"}) is None
