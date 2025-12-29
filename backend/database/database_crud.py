from fastapi import HTTPException
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


class CollectionCrud(object):

    def __init__(self, collection_name: Collection):
        """

        Parameters
        ----------
        collection_name :
        """

        self.collection_name = collection_name

    def read(self, email):
        """

        Parameters
        ----------
        email :

        Returns
        -------

        """
        return self.collection_name.find_one({"email": email})

    def delete(self, email):
        """

        Parameters
        ----------
        email :

        Returns
        -------

        """
        result = self.collection_name.delete_one({"email": email})
        if result.deleted_count == 0:
            raise HTTPException(status_code=400, detail="User does not exist")
        return result

    def create(self, datas: dict):
        """

        Parameters
        ----------
        datas :

        Returns
        -------

        """
        try:
            result = self.collection_name.insert_one(datas)
        except DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Email already exists.")
        return result

    def update(self, email, user_data):
        """

        Parameters
        ----------
        email :
        user_data :

        Returns
        -------

        """
        result = self.collection_name.update_one(
            {"email": email},
            {"$set": user_data},
            upsert=True,  # si True, crée le doc si inexistant
        )
        return result
