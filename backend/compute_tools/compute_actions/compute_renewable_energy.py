def calculate_renewable_energy_savings(housing_type: str = "apartment"):
    """
    housing_type: "apartment" ou "house"
    Gain annuel estimé pour le passage à un contrat 100% vert.
    """
    # On divise par 52 si on veut le gain par semaine,
    # ou on laisse l'impact annuel si c'est une action 'One Shot'.
    # Pour ton MVP, restons sur le gain annuel d'un coup !
    if housing_type == "house":
        return 0.500  # 500 kg soit 0.5 tonne
    return 0.200  # 200 kg soit 0.2 tonne
