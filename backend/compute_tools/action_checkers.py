import datetime

from backend.compute_tools.compute_actions import (
    compute_bicycle,
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
    def __init__(self, act_info):
        self.act_info = act_info
        self.contribution = 0

        if "name" in self.act_info.keys():
            if self.act_info["name"] == "reduce_car_use_bicycle":

                self.impact = self.is_bike()
            elif self.act_info["name"] == "reduce_car_use_public_transport":
                self.impact = self.is_public_tranport()
            else:
                self.impact = 0

    def is_bike(self):
        return compute_bicycle.impact_voiture(
            self.act_info["info"]["address_a"],
            self.act_info["info"]["address_b"],
            self.act_info["info"]["type"],
        )["emissions_tCO2e"]

    def is_public_tranport(self):

        return public_transport.co2_transport(
            self.act_info["info"]["address_a"],
            self.act_info["info"]["address_b"],
            self.act_info["info"]["type"],
        )
