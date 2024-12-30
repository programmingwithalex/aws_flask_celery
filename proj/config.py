import os


class BaseConfig:
    """base configuration"""
    TESTING = False

    SECRET_KEY = os.environ['FLASK_SECRET_KEY']  # necessary for `flask.flash`


class DevelopmentConfig(BaseConfig):
    """development configuration"""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """production configuration"""

    DEBUG = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.office365.com"
    MAIL_PORT = os.environ.get("MAIL_PORT") or 587
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_APP_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
