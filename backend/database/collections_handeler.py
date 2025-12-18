from backend.database import database_configs, database_crud


class ClientCollection(database_crud.CollectionCrud):
    """only password and email"""

    collection_name = (
        database_configs.client_accounts_collection
    )  # client_collection = db["client"]

    def __init__(self):
        super().__init__(ClientCollection.collection_name)

    def add_new_user(self, user_data):
        """

        Parameters
        ----------
        user_data :

        Returns
        -------

        """
        self.create(user_data.model_dump())

    def update_user_connexions_info(self, email, user_data):
        """

        Parameters
        ----------
        email :
        user_data :

        Returns
        -------

        """
        self.update(email, user_data)


class UserProfileInfos(database_crud.CollectionCrud):
    """handeling user profiles"""

    user_profile_infos_collection = (
        database_configs.user_profile_infos_collection
    )  # user_profile_infos_collection = db["user_profile"]

    def __init__(self):
        super().__init__(UserProfileInfos.user_profile_infos_collection)

    def add_update_user_profile_informations(self, user_data):

        self.update(user_data["email"], user_data)

    def add_update_user_informations(self, user_data):
        """

        Parameters
        ----------
        user_data :

        Returns
        -------

        """
        user_data_dict = user_data.model_dump()
        email = user_data_dict["email"]
        user_id = database_configs.client_accounts_collection.find_one(
            {"email": email}
        )["_id"]

        document = self.read(email)

        if document is not None:
            user_data_dict["_id"] = document["_id"]
            # user_profile_infos_collection.replace_one({"_id": ObjectId(document["_id"])}, user_data_dict)
            self.update(email, user_data_dict)
        else:

            user_data_dict["_id"] = user_id
            self.create(user_data_dict)
            # user_profile_infos_collection.insert_one(user_data_dict)


class ClientActions(database_crud.CollectionCrud):

    client_infos_collection = (
        database_configs.client_actions_collection
    )  # client_infos_collection = db["client_actions"]

    def __init__(self):
        super().__init__(ClientActions.client_infos_collection)
