from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
    
app = Flask(__name__)

Bootstrap(app)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI']=''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from myshop.models import User
    return User.query.get(int(user_id))

app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']=''
app.config['RECAPTCHA_PRIVATE_KEY']=''
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}



from myshop import routes
