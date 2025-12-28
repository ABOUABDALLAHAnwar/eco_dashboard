from backend.compute_tools import quartier_cordonnes
from backend.compute_tools.compute_actions import car_transport
from backend.scripts.variables import factors


# Calcul CO2
def co2_emission(distance_km, transport="public", car_type=None):

    if transport == "car" and car_type:
        return distance_km * factors[car_type]
    return distance_km * factors.get(transport, 0.05)


# Fonction principale
def co2_transport(address_a: str, address_b: str, car_type="moyenne") -> float:
    """
    calcul la difference de tco2e emis par voiture comparé au transport public
    Parameters
    ----------
    address_a
    address_b
    car_type

    Returns
    -------

    """

    lat1, lon1 = quartier_cordonnes.get_coords(address_a)
    lat2, lon2 = quartier_cordonnes.get_coords(address_b)

    # Distance sur route
    distance_km = car_transport.get_distance_osrm(
        lat1, lon1, lat2, lon2, mode="driving"
    )

    # CO2 en kg
    co2_car_kg = co2_emission(distance_km, transport="car", car_type=car_type)
    co2_public_kg = co2_emission(distance_km, transport="public")

    # CO2 évité en tCO2e
    co2_tonne = (co2_car_kg - co2_public_kg) / 1000

    return co2_tonne
