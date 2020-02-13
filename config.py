import os

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

REDIS_ROOMS_DECODE_RESPONSES = True
REDIS_ROOMS_URL = os.environ.get("REDIS_URL")
