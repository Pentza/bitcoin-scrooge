import os
from dotenv import load_dotenv

# This requires you to have .env file with SECRET in it
# secret can be generated f.e. with secrets.token_hex() -method
load_dotenv()

SECRET = os.getenv('SECRET')
