from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '827&&&&#*@&**((8@@!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hungqazsdf123@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 2

db = SQLAlchemy(app=app)


cloudinary.config(
    cloud_name = 'dv3klmst5',
    api_key = '648287616742351',
    api_secret = 'HLWzHDfuMGO4aHZLc0pykLoJuhM'
)

login = LoginManager(app=app)