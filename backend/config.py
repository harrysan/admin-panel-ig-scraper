from dotenv import load_dotenv
import os

class Config:
    load_dotenv()
    url = 'mysql+pymysql://'+os.environ['userdb']+':'+os.environ['passdb']+'@localhost/'+os.environ['database']
    SQLALCHEMY_DATABASE_URI = url
    SQLALCHEMY_TRACK_MODIFICATIONS = False