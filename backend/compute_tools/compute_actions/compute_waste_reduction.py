"""
Clé (Backend),Nom (Frontend),Concept,Impact (kg CO2​e)
compost,Compostage,Déchets organiques détournés de l'incinération.,~1.5 kg
recycling,Tri Sélectif,Emballages (plastique/métal) envoyés au recyclage.,~2.0 kg
glass,Recyclage Verre,Bouteilles déposées en borne de récupération.,~0.8 kg
bulk_shopping,Achat en Vrac,Suppression des emballages à la source (courses).,~1.2 kg


ensuite pour chaue fonction voici l'idee :
L'idée est de rester sur des unités visuelles (le contenant) plutôt que sur du poids.

1. Le Compost (calculate_compost_savings)
Donnée à demander : Le nombre de bioseaux (ou petits bacs de cuisine) vidés.

Pourquoi ? C'est l'unité que tout le monde visualise.

Calcul : Nombre de seaux × 1.5 kg CO2e.

Variable simple : nb_buckets (int).

2. Le Tri Sélectif / Recyclage (calculate_recycling_savings)
Donnée à demander : La taille de la poubelle jaune vidée.

Pourquoi ? On sait tous si on vide une petite poubelle de cuisine (30L) ou un grand bac d'immeuble.

Options simples : Un choix entre "Petite (30L)" ou "Grande (50L+)".

Variable simple : bin_size (string: "small" ou "large").

3. Le Verre (calculate_glass_savings)
Donnée à demander : Le volume approximatif (un sac ou un panier).

Pourquoi ? On attend souvent d'avoir un sac plein avant d'aller à la borne à verre.

Calcul : Un forfait par "apport" à la borne.

Variable simple : Juste un clic de validation (on considère un apport moyen de 5-8 bouteilles).

"""


def calculate_bulk_savings(is_family_size: bool = False):
    """
    Calcule l'économie de CO2 pour une semaine de courses en vrac.
    On évite principalement la production de plastique et carton.
    """
    # Base : 1.2 kg de CO2 évité pour une personne seule par semaine
    base_savings = 1.2

    # Si c'est pour une famille, on applique un coefficient d'échelle
    # On ne fait pas x4 (car on achète souvent en plus gros formats de base)
    # mais on augmente significativement l'impact.
    multiplier = 2.5 if is_family_size else 1.0

    total_kg = base_savings * multiplier

    # Retour en tonnes pour ton dashboard
    return total_kg / 1000


def calculate_compost_savings(nb_buckets: int = 1):
    """
    nb_buckets: Nombre de petits seaux de cuisine (~3kg chacun)
    Un geste très efficace pour éviter le méthane en décharge.
    """
    impact_per_bucket = 1.5  # kg CO2e
    return (nb_buckets * impact_per_bucket) / 1000


def calculate_recycling_savings(bin_size: str = "small"):
    """
    bin_size: "small" (~30L) ou "large" (~50L)
    Le recyclage plastique/métal est très gratifiant en CO2.
    """
    # On définit le poids moyen par taille de poubelle
    weight = 3.0 if bin_size == "small" else 5.5
    impact_per_kg = 1.2

    return (weight * impact_per_kg) / 1000


def calculate_glass_savings():
    """
    On reste sur un geste forfaitaire (un sac de bouteilles apporté).
    Le verre est lourd mais son recyclage est très efficace.
    """
    # Forfait : ~0.8 kg de CO2e par sac de bouteilles
    return 0.8 / 1000


# backend/core/waste/service.py


def calculate_weekly_waste_reduction(data: dict):
    """
    Calcule l'impact total d'un bilan hebdomadaire de déchets.
    Le dictionnaire 'data' contient les réponses du formulaire.
    """
    total_tonnes = 0

    # 1. Calcul Vrac
    if data.get("bulk_done"):
        is_family = data.get("is_family", False)
        total_tonnes += calculate_bulk_savings(is_family)

    # 2. Calcul Compost
    nb_buckets = data.get("compost_buckets", 0)
    if nb_buckets > 0:
        total_tonnes += calculate_compost_savings(nb_buckets)

    # 3. Calcul Recyclage
    if data.get("recycling_done"):
        size = data.get("recycling_bin_size", "small")
        total_tonnes += calculate_recycling_savings(size)

    # 4. Calcul Verre
    nb_glass_trips = data.get(
        "glass_trips", 0
    )  # On peut en faire plusieurs par semaine
    for _ in range(nb_glass_trips):
        total_tonnes += calculate_glass_savings()

    return total_tonnes
