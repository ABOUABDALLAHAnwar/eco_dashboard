import backend.scripts.variables as cfg  # remplace par le nom réel du fichier

def test_configs_import():
    # juste importer et vérifier les variables
    assert cfg.ALGORITHM == "HS256"
    assert cfg.ACCESS_TOKEN_EXPIRE_MINUTES == 300

    # vérifier que les dictionnaires existent
    assert "petite" in cfg.facteurs
    assert "bus" in cfg.factors
