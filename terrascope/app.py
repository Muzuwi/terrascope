import os
from flask import Flask
import logging

import terrascope.config
import terrascope.db
import terrascope.services.visualizer
import terrascope.services.world_listener
from .config import BaseConfig
from .frontend import frontend
from .utils import INSTANCE_FOLDER_PATH, pretty_date
from .api import snapshots

# For import *
__all__ = ["create_app"]

DEFAULT_BLUEPRINTS = (frontend, snapshots.blueprint)


def create_app(config=None, app_name=None, blueprints=None):
    # Create a Flask app
    if app_name is None:
        app_name = BaseConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(
        app_name, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True
    )

    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_template_filters(app)
    configure_error_handlers(app)

    logging.basicConfig(level=logging.DEBUG)
    terrascope.db.init(app)
    terrascope.services.world_listener.init(
        app, terrascope.services.visualizer.visualize
    )
    terrascope.services.visualizer.init(app)

    return app


def configure_app(app: Flask, config: terrascope.config.BaseConfig = None):
    # apply the default config
    app.config.from_object(BaseConfig)
    # apply custom modifications next
    if config:
        app.config.from_object(config)
    # allow overlaying the config using env variables
    for v in vars(BaseConfig):
        if v in os.environ:
            cls = type(getattr(BaseConfig, v))
            app.config[v] = cls(os.environ[v])

    # sanity checks
    if app.config["SECRET_KEY"] == "":
        raise RuntimeError(
            "'SECRET_KEY' was not provided in the configuration. "
            "This must be set to a long random bytestring. You can generate one by running: "
            "python -c 'import secrets; print(secrets.token_hex())'"
        )
    if app.config["TERRASCOPE_DATA_DIRECTORY"] == "":
        raise RuntimeError(
            "'TERRASCOPE_DATA_DIRECTORY' was not provided in the configuration. "
            "This must point to a folder somewhere on the filesystem where database "
            "and captures will be stored at."
        )


def configure_blueprints(app, blueprints):
    # Configure blueprints in views
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_template_filters(app):
    @app.template_filter()
    def _pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format="%Y-%m-%d"):
        return value.strftime(format)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        return "Oops! You don't have permission to access this page.", 403

    @app.errorhandler(404)
    def page_not_found(error):
        return "Opps! Page not found.", 404

    @app.errorhandler(500)
    def server_error_page(error):
        return "Oops! Internal server error. Please try after sometime.", 500
