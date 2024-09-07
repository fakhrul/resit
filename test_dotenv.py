import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

print(os.environ.get('DOMAIN'))
print(os.environ.get('ADMIN_EMAIL'))