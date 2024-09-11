from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


__db = SQLAlchemy(model_class=Base)


def getdb() -> SQLAlchemy:
    return __db


def init(app: Flask):
    # import all models
    from .model.snapshot import WorldSnapshot

    __db.init_app(app)
    with app.app_context():
        __db.create_all()
