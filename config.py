import os

import dotenv

dotenv.load_dotenv('config.env')

TOKEN = os.environ.get('TOKEN')
