import datetime

from backend.compute_tools.compute_actions import (
    compute_bicycle,
    compute_plant_based_diet,
    compute_renewable_energy,
    compute_tree_planting,
    compute_waste_reduction,
    public_transport,
)


def create_liste_time():
    return [
        datetime.datetime.now().time().hour,
        datetime.datetime.now().time().minute,
        datetime.datetime.now().time().second,
    ]


def create_liste_ymd_hms():
    now = datetime.datetime.now()
    return [now.year, now.month, now.day, now.hour, now.minute, now.second]


class ActionChecker:
    def __init__(self, act_info, age=None):
        self.act_info = act_info
        self.age = age
        self.contribution = 0
        self.action_map = {
            "reduce_car_use_bicycle": self.is_bike,
            "reduce_car_use_public_transport": self.is_public_transport,
            "plant_based_diet": self.is_plant_based_diet,
            "waste_reduction": self.is_waste_reduction,
            "tree_planting": self.is_tree_planting,
            "renewable_energy": self.is_renewable_energy,
        }

        # Dispatcher : On cherche l'action, sinon 0
        action_name = self.act_info.get("name")
        handler = self.action_map.get(action_name)

        if handler:
            self.impact = handler()
        else:
            self.impact = 0

    def is_bike(self):
        return compute_bicycle.impact_voiture(
            self.act_info["info"]["address_a"],
            self.act_info["info"]["address_b"],
            self.act_info["info"]["type"],
        )["emissions_tCO2e"]

    def is_public_transport(self):

        return public_transport.co2_transport(
            self.act_info["info"]["address_a"],
            self.act_info["info"]["address_b"],
            self.act_info["info"]["type"],
        )

    def is_plant_based_diet(self):
        return compute_plant_based_diet.calculate_multiple_diet_savings(
            self.act_info["info"]["meals_replaced"],
            self.act_info["info"]["meals_consumed"],
            self.age,
        )

    def is_waste_reduction(self):
        return compute_waste_reduction.calculate_weekly_waste_reduction(
            self.act_info["info"]
        )

    def is_tree_planting(self):
        return compute_tree_planting.calculate_tree_planting(self.act_info["info"])

    def is_renewable_energy(self):
        return compute_renewable_energy.calculate_renewable_energy_savings(
            self.act_info["info"]
        )
