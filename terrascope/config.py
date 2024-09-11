import os


class BaseConfig(object):
    """Configuration keys used by terrascope

    These are stored in app.config, but this class serves as documentation
    for all possible configuration options. These values can also be overridden
    using identically named environment variables. The string value of the envvar
    is casted to the type of the field as defined here.
    """

    PROJECT: str = "terrascope"
    PROJECT_NAME: str = "terrascope.muzuwi.dev"
    PROJECT_ROOT: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    BASE_URL: str = "https://github.com/muzuwi/terrascope"
    TESTING: bool = False
    # Flask-cache
    CACHE_TYPE: str = "simple"
    CACHE_DEFAULT_TIMEOUT: int = 60

    # All variables below can be freely changed when deploying terrascope
    DEBUG: bool = True
    SECRET_KEY: str = ""
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///terrascope.db"
    # terrascope-specific
    TERRASCOPE_WORLD_DIRECTORY: str = ""
    TERRASCOPE_DATA_DIRECTORY: str = ""
