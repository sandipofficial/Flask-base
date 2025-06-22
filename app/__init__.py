from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'super secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MatthieuOctobre10__'
app.config['MYSQL_DB'] = 'epytododb'
app.config['TESTING'] = False

mysql = MySQL(app)

from app import views