def hash_pw(password: str) -> str:
    # Placeholder for hashing function, replace with actual hashing (e.g., bcrypt)
    return "hashed_" + password

def verify_pw(password: str, hashed_password: str) -> bool:
    # Placeholder for password verification function
    return hash_pw(password) == hashed_password