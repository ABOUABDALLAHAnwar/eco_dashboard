import datetime
from pydantic import BaseModel


class User(BaseModel):
    email: str
    hashed_password: str


class Profile(BaseModel):
    _id: str
    name: str
    position: str
    about: str
    age: int
    country: str
    address: str
    email: str
    phone: str
    status: int
    first_update_day: list
    first_update_hour: list
    last_update_day: list
    last_update_hour: list


class Users_profile:

    def __init__(
        self,
        name: str,
        position: str,
        about: str,
        age: int,
        country: str,
        address: str,
        phone: str,
        email: str,
        id: str,
    ):

        self.first_update_day = [
            datetime.datetime.now().year,
            datetime.datetime.now().month,
            datetime.datetime.now().day,
        ]
        self.first_update_hour = [
            datetime.datetime.now().time().hour,
            datetime.datetime.now().time().minute,
            datetime.datetime.now().time().second,
        ]

        self.last_update_day = [
            datetime.datetime.now().year,
            datetime.datetime.now().month,
            datetime.datetime.now().day,
        ]
        self.last_update_hour = [
            datetime.datetime.now().time().hour,
            datetime.datetime.now().time().minute,
            datetime.datetime.now().time().second,
        ]
        self.status = 1
        self.name = name
        self.position = position
        self.about = about
        self.age = age
        self.country = country
        self.address = address
        self.phone = phone
        self.email = email
        self.id = id

        self.prof = Profile(
            _id=self.id,
            name=self.name,
            position=self.position,
            about=self.about,
            age=self.age,
            country=self.country,
            address=self.address,
            email=self.email,
            phone=self.phone,
            status=self.status,
            first_update_day=self.first_update_day,
            first_update_hour=self.first_update_hour,
            last_update_day=self.last_update_day,
            last_update_hour=self.last_update_hour,
        )

        self.prof_dict = (
            self.prof.model_dump()
        )  # ou prof.model_dump() si tu es en Pydantic v2
