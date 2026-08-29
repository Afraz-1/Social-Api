from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash(password:str):
    hasedpass = pwd_context.hash(password)
    return hasedpass

def verify(userpassword,hashedpass):
    return pwd_context.verify(userpassword,hashedpass)