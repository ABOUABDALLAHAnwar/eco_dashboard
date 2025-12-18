import datetime

from backend.compute_tools import compute_bicycle
from backend.database import collections_handeler


class MultipleCollection:

    client = collections_handeler.ClientCollection()
    userprofile = collections_handeler.UserProfileInfos()
    actions = collections_handeler.ClientActions()

    def get_all_datas(self, email):
        """

        Parameters
        ----------
        email :

        Returns
        -------

        """

        client_information = self.client.read(email)

        user_profile = self.userprofile.read(email)
        result = {
            "client_information": client_information,
            "user_profile": user_profile,
        }

        return result

    def add_user_action(self, email, act_info):
        """

        Parameters
        ----------
        email :
        act_info :

        Returns
        -------

        """

        user_profile = self.userprofile.read(email)
        user_actions = self.actions.read(email)

        tco2e_action_per_action = 0
        if "name" in act_info.keys(
        ) and act_info["name"] == "reduce_car_use_bicycle":
            tco2e_action_per_action = compute_bicycle.impact_voiture(
                act_info["info"]["distance"], act_info["info"]["type"]
            )["emissions_tCO2e"]

        if user_actions is None:
            user_actions = {
                "_id": user_profile["_id"],
                "first_update_hour": [
                    datetime.datetime.now().time().hour,
                    datetime.datetime.now().time().minute,
                    datetime.datetime.now().time().second,
                ],
                "action": [
                    dict(
                        action_date=[
                            datetime.datetime.now().time().hour,
                            datetime.datetime.now().time().minute,
                            datetime.datetime.now().time().second,
                        ],
                        action=act_info,
                        tco2e_action=tco2e_action_per_action,
                    )
                ],
                "tco2e_total": tco2e_action_per_action,
                "email": email,
            }
            self.actions.client_infos_collection.insert_one(user_actions)

        else:
            user_actions["action"].append(
                dict(
                    action_date=[
                        datetime.datetime.now().time().hour,
                        datetime.datetime.now().time().minute,
                        datetime.datetime.now().time().second,
                    ],
                    action=act_info,
                    tco2e_action=tco2e_action_per_action,
                )
            )

            user_actions["tco2e_total"] = (
                user_actions["tco2e_total"] + user_actions["action"][-1]["tco2e_action"]
            )
            self.actions.client_infos_collection.update_one(
                {"_id": user_profile["_id"]}, {"$set": user_actions}
            )

        return user_actions
