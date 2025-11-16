import bcrypt

def hash_password(pwd: str, roudns:int = 10) -> str:
    salt = bcrypt.gensalt(rounds = roudns)
    hasedPassword = bcrypt.hashpw(pwd.encode("utf-8"), salt).decode("utf-8")
    return hasedPassword
    