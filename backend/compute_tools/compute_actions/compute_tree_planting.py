def calculate_tree_planting(nb_trees: int = 1):
    """
    nb_trees: Nombre d'arbres plantés.
    Impact : 25kg CO2 par arbre et par an.
    """
    impact_per_tree = 25.0
    return (nb_trees * impact_per_tree) / 1000  # Retourne en tonnes
