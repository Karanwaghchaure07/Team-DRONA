import bcrypt
import json

# Sample users
users = [
    {
        "username": "admin",
        "password": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    },
    {
        "username": "user1",
        "password": bcrypt.hashpw("password1".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    }
]

# Save to JSON file
with open('users.json', 'w') as f:
    json.dump({"users": users}, f, indent=4)

print("Users have been created and saved to users.json.")
