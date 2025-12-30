import os

class Config:
    SECRET_KEY = "minimart-secret-key"
    MONGO_URI = "mongodb://localhost:27017/minimart"
import os

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

class Config:
    SECRET_KEY = "minimart-secret-key"
    MONGO_URI = "mongodb://localhost:27017/minimart"
    UPLOAD_FOLDER = UPLOAD_FOLDER
