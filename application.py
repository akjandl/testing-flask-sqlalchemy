from flask import Flask

from secrets import DATABASE_URI
from db import db
from api import models  # importing models is required to load models. must be after db import
from api.routes import routes_blueprint

app = Flask(__name__)
app.register_blueprint(routes_blueprint)


def create_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


if __name__ == "__main__":
    application = create_app(app)
    application.run()
