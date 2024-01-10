import os
from dotenv import load_dotenv

dotenv_path = os.path.join(f"{os.path.dirname(__file__)}/..", '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError('No .env file found')


class Config(object):
    token: str = os.environ.get('TOKEN')
