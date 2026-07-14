import hashlib
from db import get_users, add_user, get_user_data

def hash_password(password):
    """Hashes a password string using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(username, password, email, role, full_name):
    """Registers a user by hashing their password and storing it in the database."""
    if not username or not password or not email or not full_name:
        return False, "All fields are required!"
    
    users = get_users()
    if username in users:
        return False, "Username already exists!"
    
    password_hash = hash_password(password)
    success = add_user(username, password_hash, email, role, full_name)
    if success:
        return True, "Registration successful! Please log in."
    else:
        return False, "Registration failed. Please try again."

def authenticate_user(username, password):
    """Verifies credentials. Returns the user details if successful, otherwise None."""
    if not username or not password:
        return None
    
    users = get_users()
    if username not in users:
        return None
    
    password_hash = hash_password(password)
    stored_hash = users[username].get("password_hash")
    
    if password_hash == stored_hash:
        return get_user_data(username)
    
    return None
