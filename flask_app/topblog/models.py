from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return self.__str__


class PostModel(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(65), nullable=False)
    subtitle = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    created_time = db.Column(db.String(250), nullable=False)
    updated_time = db.Column(db.String(250), nullable=False)

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return self.__str__
