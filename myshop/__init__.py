from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
    
app = Flask(__name__)

Bootstrap(app)
app.config['SECRET_KEY'] = '58be938844c3e73b40850dd2f170ed237a45588f70d5a825'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://c1743324:530337@csmysql.cs.cf.ac.uk:3306/c1743324'
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
app.config['RECAPTCHA_PUBLIC_KEY']='6LfmRJkUAAAAAB-jCiByLXJW8QDlY5KKuXDpnN2L'
app.config['RECAPTCHA_PRIVATE_KEY']='6LfmRJkUAAAAABD1z1hqeHJB7dqok1qxy8N2QEuw'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}



from myshop import routes
