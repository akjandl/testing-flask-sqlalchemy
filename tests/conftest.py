import pytest
from mixer.backend.flask import mixer

from application import app as flask_application
from db import db
from secrets import DATABASE_TEST_URI


flask_application.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_TEST_URI
flask_application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
flask_application.config["TESTING"] = True
db.init_app(flask_application)


@pytest.fixture()
def app():
    with flask_application.app_context():
        db.create_all()

        yield flask_application

        # explicitly close session or process hangs on cleanup
        # SEE:
        #   https://stackoverflow.com/questions/26350911/what-to-do-when-a-py-test-hangs-silently
        #   https://docs.sqlalchemy.org/en/13/faq/metadata_schema.html#my-program-is-hanging-when-i-say-table-drop-metadata-drop-all
        db.session.close()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def app_mixer(app):
    mixer.init_app(app)
    return mixer
