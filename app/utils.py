from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def hash(password:str):
    return password_hash.hash(password)

def verify(userpassword,hashedpass):
    return password_hash.verify(userpassword,hashedpass)