import os
import secrets

DATA_FILE = 'storage/data.json'
MAX_USERNAME_LENGTH = 50
MAX_MESSAGE_LENGTH = 500

SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
