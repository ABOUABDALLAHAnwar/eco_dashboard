from backend.scripts.emissions_factors import FOOD_COEFFICIENTS


def get_age_multiplier(age: int):
    """

    Parameters
    ----------
    age

    Returns
    -------

    """
    if age < 12:
        return 0.6
    if 12 <= age <= 30:
        return 1.2
    if 31 <= age <= 60:
        return 1.0
    return 0.8


def calculate_diet_savings(meal_replaced: str, meal_consumed: str, age: int):
    # Par défaut, on compare au Boeuf si inconnu (pire scénario)
    impact_before = FOOD_COEFFICIENTS.get(meal_replaced, 6.50)
    impact_after = FOOD_COEFFICIENTS.get(meal_consumed, 0.40)

    # Calcul du gain net en tonnes (pour ton Dashboard)
    # 1 kg = 0.001 tonne
    multiplier = get_age_multiplier(age)
    diff_kg = multiplier * (impact_before - impact_after)

    return max(0, diff_kg / 1000)


def calculate_multiple_diet_savings(
    meals_replaced: list[str], meals_consumed: list[str], age: int
):
    """

    Parameters
    ----------
    meals_replaced
    meals_consumed
    age

    Returns
    -------

    """
    if len(meals_replaced) != len(meals_consumed):
        raise ValueError("Les deux listes doivent avoir la même taille.")

    multiplier = get_age_multiplier(age)
    total_diff_kg = 0

    for replaced, consumed in zip(meals_replaced, meals_consumed):
        impact_before = FOOD_COEFFICIENTS.get(replaced, 6.50)
        impact_after = FOOD_COEFFICIENTS.get(consumed, 0.40)

        total_diff_kg += multiplier * (impact_before - impact_after)

    return max(0, total_diff_kg / 1000)
