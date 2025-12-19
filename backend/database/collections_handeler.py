from backend.database import database_configs, database_crud


class ClientCollection(database_crud.CollectionCrud):
    """only password and email"""


    def __init__(self, collection_name=None):
        """

        Parameters
        ----------
        collection_name :
        """
        if collection_name is None:
            collection_name = database_configs.client_accounts_collection
        super().__init__(collection_name)

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
        self.update(email, user_data.model_dump())


class UserProfileInfos(database_crud.CollectionCrud):
    """handeling user profiles"""

    def __init__(self, collection_name=None):
        """

        Parameters
        ----------
        collection_name :

        Returns
        -------

        """
        if collection_name is None:
            collection_name = (
                database_configs.user_profile_infos_collection
            )
        super().__init__(collection_name)

    def add_update_user_profile_informations(self, user_data):
        user_data_dict = user_data.model_dump()

        self.update(user_data_dict["email"], user_data_dict)

    def add_update_user_informations(self, user_data, client_accounts_collection=None):
        """

        Parameters
        ----------
        user_data :
        client_accounts_collection :

        Returns
        -------

        """
        if client_accounts_collection is None :
            client_accounts_collection = database_configs.client_accounts_collection

        user_data_dict = user_data.model_dump()
        email = user_data_dict["email"]

        user_id = client_accounts_collection.find_one(
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

    def __init__(self, collection_name=None):
        """

        Parameters
        ----------
        collection_name :
        """
        if collection_name is None:
            collection_name = (
                database_configs.client_actions_collection
            )  # client_infos_collection = db["client_actions"]

        self.collection_name = collection_name
        super().__init__(collection_name)
