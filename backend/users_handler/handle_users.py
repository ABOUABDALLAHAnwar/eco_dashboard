from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserSignin:
    def __init__(self, password, hashed_password=None):
        self.checker = True
        self.password = password
        self.password_check()
        self.hashed = self.hash_password()
        if hashed_password is not None:
            self.hashed_password = hashed_password

    def password_check(self):
        if len(self.password) < 8:
            self.checker = False

    def hash_password(self):
        return pwd_context.hash(self.password)
