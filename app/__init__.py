from flask import Flask
from flask_mail         import Mail
from flask_bcrypt       import Bcrypt
from flask_qrcode       import QRcode
from flask_sqlalchemy   import SQLAlchemy
from flask_login        import LoginManager

app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://projet:tejorp@localhost/projet'
app.config['SECRET_KEY'] = '@/Secret---Key@@'

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'miniprojet.faikahm@gmail.com',
    MAIL_PASSWORD = 'AhmedYassineFAIKM1Info',
))

db            = SQLAlchemy(app)
bcrypt        = Bcrypt(app)
mail          = Mail(app)
qrcode        = QRcode(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app import routes