import os


class Config:
    DEBUG = False
    TESTING = False
    API_KEY = os.getenv("WEATHER_API_KEY")
    API_URL = os.getenv("WEATHER_API_URL")
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379


class DevelopmentGonfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    REDIS_HOST = os.getenv("REDIS_HOST", "prod-redis-host")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))