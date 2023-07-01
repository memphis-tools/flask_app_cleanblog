import os
from dotenv import load_dotenv


# app mandatory custom vars
DEFAULT_DB_URI = "blog.db"
DEFAULT_APP = "topblog"
POST_PAGINATOR_MAX = 5
LOREM_PICSUM_URIS_RANDOM_RANGE = 200

# app mandatory default vars
load_dotenv(".envrc")
TESTING = True
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEFAULT_DB_URI}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
