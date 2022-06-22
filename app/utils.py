from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def passwd_hash(password):
    return pwd_context.hash(password)


def verify_passwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
