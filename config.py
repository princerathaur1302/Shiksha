import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///siksha_academy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False