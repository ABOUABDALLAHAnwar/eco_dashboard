from fastapi import APIRouter

from backend.compute_tools import full_datas_aggregation, quartier_cordonnes

router = APIRouter(tags=["aggregation_dashboard"])


@router.get("/get_dashboard_full_data")
async def get_dashboard_full_data():
    """

    Returns
    -------

    """
    users_per_city, tco2e_per_city = full_datas_aggregation.aggregate_datas()

    table_users_by_city = [[city, len(users)] for city, users in users_per_city.items()]

    table_tco2e_by_city = [[city, total] for city, total in tco2e_per_city.items()]

    all_cities = set(city for city, _ in table_users_by_city).union(
        city for city, _ in table_tco2e_by_city
    )

    users_dict = dict(table_users_by_city)
    tco2e_dict = dict(table_tco2e_by_city)

    joined_table = [
        [city, users_dict.get(city, 0), tco2e_dict.get(city, 0.0)]
        for city in all_cities
    ]
    return joined_table


@router.get("/get_dashboard_quartier_data")
async def get_dashboard_quartier_data():
    return full_datas_aggregation.aggregate_by_neighbourhood()


@router.get("/get_coordinate/{city}")
async def get_coordinate_city(city: str):
    return quartier_cordonnes.get_coords(city)
