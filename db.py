import os
import json

# Define path to local JSON database inside the project directory
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

def init_db():
    """Initializes the JSON database file with default collections if it does not exist."""
    if not os.path.exists(DB_FILE):
        default_data = {
            "users": {},
            "grades": {},
            "attendance": {},
            "tasks": {}
        }
        with open(DB_FILE, "w") as f:
            json.dump(default_data, f, indent=4)

def load_db():
    """Loads the JSON database content into memory."""
    init_db()
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading database: {e}")
        return {"users": {}, "grades": {}, "attendance": {}, "tasks": {}}

def save_db(data):
    """Saves database content to the JSON file."""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving database: {e}")
        return False

def get_users():
    """Retrieves all users dictionary."""
    db = load_db()
    return db.get("users", {})

def add_user(username, password_hash, email, role, full_name):
    """Adds a new user and pre-populates default smart campus metric data."""
    db = load_db()
    if username in db["users"]:
        return False
    
    # Store credentials
    db["users"][username] = {
        "password_hash": password_hash,
        "email": email,
        "role": role,
        "full_name": full_name
    }
    
    # Pre-populate student/faculty sample data
    db["attendance"][username] = 92.5
    db["grades"][username] = [
        {"course": "Introduction to AI", "grade": "A", "gpa": 4.0},
        {"course": "Database Systems", "grade": "A-", "gpa": 3.7},
        {"course": "Data Structures & Algorithms", "grade": "B+", "gpa": 3.3},
        {"course": "Software Engineering Project", "grade": "A", "gpa": 4.0}
    ]
    db["tasks"][username] = [
        {"id": 1, "title": "Submit AI Lab 3 (Neural Networks)", "due": "2026-07-20", "status": "Pending"},
        {"id": 2, "title": "Complete Database Design Assignment", "due": "2026-07-22", "status": "Completed"},
        {"id": 3, "title": "Review Software Architecture Patterns", "due": "2026-07-18", "status": "Pending"}
    ]
    
    return save_db(db)

def get_user_data(username):
    """Fetches comprehensive profile details and campus data for a user."""
    db = load_db()
    user_info = db["users"].get(username, {})
    if not user_info:
        return None
    
    return {
        "username": username,
        "email": user_info.get("email"),
        "role": user_info.get("role"),
        "full_name": user_info.get("full_name"),
        "attendance": db["attendance"].get(username, 100.0),
        "grades": db["grades"].get(username, []),
        "tasks": db["tasks"].get(username, [])
    }

def update_user_tasks(username, tasks):
    """Updates a user's task list."""
    db = load_db()
    if username in db["users"]:
        db["tasks"][username] = tasks
        return save_db(db)
    return False
