import os


class Config(object):
    """
    Base config
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAX_NUMBER_OF_PEOPLE_ALLOWED = 10000
    NUMBER_OF_WORKERS = 3
    NUMBER_OF_BEST_MATCHES_TO_RETURN = 3
    FIXED_SIZE_VECTOR = 256
    MONGO_URI = "mongodb://localhost:27017/my-mongodb"


class ProductionConfig(Config):
    DEBUG = False
    # Adjust accordingly to resources...
    MAX_NUMBER_OF_PEOPLE_ALLOWED = 10000
    NUMBER_OF_WORKERS = 3
    NUMBER_OF_BEST_MATCHES_TO_RETURN = 3
    FIXED_SIZE_VECTOR = 256
    MONGO_URI = "mongodb://localhost:27017/my-mongodb"


class DevelopmentConfig(Config):
    """
    Development config - enables debugging
    """
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
    # Adjust accordingly to resources...
    MAX_NUMBER_OF_PEOPLE_ALLOWED = 10000
    NUMBER_OF_WORKERS = 3
    NUMBER_OF_BEST_MATCHES_TO_RETURN = 3
    FIXED_SIZE_VECTOR = 256
    MONGO_URI = "mongodb://localhost:27017/my-mongodb"
