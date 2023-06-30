from .topblog import models
from .topblog.views import app

models.db.init_app(app)


@app.cli.command("init_the_db")
def init_db():
    with app.app_context():
        models.db.init_app(app)
        models.db.drop_all()
        models.db.create_all()
