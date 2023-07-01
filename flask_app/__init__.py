import os
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

from .topblog.settings import DEFAULT_APP, DEFAULT_DB_URI, LOREM_PICSUM_URIS_RANDOM_RANGE
from .topblog import models
from .topblog.views import app

models.db.init_app(app)


@app.cli.command("init_the_db")
def init_db():
    db_app = DEFAULT_APP
    db_uri = DEFAULT_DB_URI
    db_file_path = f"{db_app}/{db_uri}"
    if os.path.isfile(db_file_path):
        os.remove(db_file_path)

    hashed_and_salted = generate_password_hash("applepie94", "pbkdf2:sha256", salt_length=8)
    dummy_users_list = [
        models.UserModel(username="donald.duck", email="donald.duck@bluelake.fr", password=hashed_and_salted),
        models.UserModel(username="daisy.duck", email="daisy.duck@bluelake.fr", password=hashed_and_salted),
        models.UserModel(username="loulou.duck", email="loulou.duck@bluelake.fr", password=hashed_and_salted),
    ]

    dummy_picsum_id = random.randrange(1, LOREM_PICSUM_URIS_RANDOM_RANGE)
    dummy_picsum_url = f"https://picsum.photos/id/{dummy_picsum_id}/1900/1267"
    today = datetime.today()
    dummy_post = models.PostModel(title="Once upon a time",
                                  subtitle="..,in a far galaxy",
                                  description="""
                    Maecenas cursus nisi eget ipsum auctor, quis faucibus lorem volutpat.
                    Quisque luctus auctor odio, nec tempus erat vehicula et. Aenean vel finibus quam.
                    Sed euismod eros rhoncus est feugiat tincidunt. Praesent ex diam, dignissim a massa nec.
                    Ullamcorper fermentum arcu, augue dui eleifend metus, non pulvinar dolor odio id.
                    """,
                                  img_url=dummy_picsum_url,
                                  author_id=2,
                                  created_time=today.strftime("%B %d, %Y"),
                                  updated_time=today.strftime("%B %d, %Y")
                                  )

    with app.app_context():
        models.db.init_app(app)
        models.db.drop_all()
        models.db.create_all()
        hashed_and_salted = generate_password_hash("applepie94", "pbkdf2:sha256", salt_length=8)
        admin = models.UserModel(username="admin", email="admin@localhost", password=hashed_and_salted)
        models.db.session.add(admin)
        for user in dummy_users_list:
            models.db.session.add(user)
            models.db.session.commit()

        project = dummy_post
        models.db.session.add(project)
        models.db.session.commit()
