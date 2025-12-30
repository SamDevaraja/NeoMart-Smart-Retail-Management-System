import bcrypt
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["minimart"]

password = "admin123".encode("utf-8")

hashed = bcrypt.hashpw(password, bcrypt.gensalt())

db.users.insert_one({
    "name": "Admin",
    "email": "admin@minimart.com",
    "password": hashed,
    "role": "admin"
})

print("✅ Admin created successfully")
