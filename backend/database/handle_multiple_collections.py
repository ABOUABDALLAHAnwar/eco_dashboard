from backend.compute_tools import action_checkers
from backend.database import collections_handeler, database_configs


class MultipleCollection:

    def __init__(
        self,
        client_accounts_collection=None,
        user_profile_infos_collection=None,
        client_actions_collection=None,
    ):
        """

        Parameters
        ----------
        client_accounts_collection :
        user_profile_infos_collection :
        client_actions_collection :
        """

        if client_accounts_collection is None:
            client_accounts_collection = database_configs.client_accounts_collection
        if user_profile_infos_collection is None:
            user_profile_infos_collection = (
                database_configs.user_profile_infos_collection
            )
        if client_actions_collection is None:
            client_actions_collection = database_configs.client_actions_collection

        self.client = collections_handeler.ClientCollection(client_accounts_collection)
        self.userprofile = collections_handeler.UserProfileInfos(
            user_profile_infos_collection
        )
        self.actions = collections_handeler.ClientActions(client_actions_collection)

    def get_all_datas(self, email):
        """

        Parameters
        ----------
        email :

        Returns
        -------

        """

        client_information = self.client.read(email)
        if client_information is None:
            raise Exception("User not found")

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
        client_information = self.client.read(email)
        if client_information is None:
            raise Exception("User not found")

        user_actions = self.actions.read(email)
        act_checker = action_checkers.ActionChecker(act_info)
        tco2e_action_per_action = act_checker.impact

        if user_actions is None:

            user_actions = {
                "_id": client_information["_id"],
                "first_update_hour": action_checkers.create_liste_ymd_hms(),
                "action": [
                    dict(
                        action_date=action_checkers.create_liste_ymd_hms(),
                        action=act_info,
                        tco2e_action=tco2e_action_per_action,
                    )
                ],
                "tco2e_total": tco2e_action_per_action,
                "email": email,
            }

            self.actions.create(user_actions)
            # self.actions.client_infos_collection.insert_one(user_actions)

        else:

            user_actions["action"].append(
                dict(
                    action_date=action_checkers.create_liste_ymd_hms(),
                    action=act_info,
                    tco2e_action=tco2e_action_per_action,
                )
            )

            user_actions["tco2e_total"] = (
                user_actions["tco2e_total"] + user_actions["action"][-1]["tco2e_action"]
            )
            self.actions.collection_name.update_one(
                {"_id": client_information["_id"]}, {"$set": user_actions}
            )

        return user_actions
