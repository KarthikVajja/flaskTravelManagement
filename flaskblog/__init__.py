from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_datepicker import datepicker
import psycopg2
from sqlalchemy import MetaData, create_engine

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
datepick = datepicker(app)
app.config['SECRET_KEY'] = '0aec81145d7d32dba31e021478a643d4'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='',url='localhost',db='DMQL')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from flaskblog import routes