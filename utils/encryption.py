from django.contrib.auth.hashers import check_password, make_password


# hash_password util is used to hash a password using Django's password hashing (PBKDF2 by default).
def hash_password(raw_password: str) -> str:
    return make_password(raw_password)


# verify_password util is used to verify a raw password against a Django-hashed password.
def verify_password(raw_password: str, hashed_password: str) -> bool:
    return check_password(raw_password, hashed_password)
