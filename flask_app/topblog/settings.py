import os
from dotenv import load_dotenv


load_dotenv(".envrc")
TESTING = True
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
