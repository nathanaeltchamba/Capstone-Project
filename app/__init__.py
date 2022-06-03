from flask import Flask
from config import Config
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

moment = Moment()
db = SQLAlchemy() #ORM Object Relational Mapper
migrate = Migrate() # Transacations for Database

login = LoginManager() # this deals with the login sessions
mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # init commands to flask
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # Flask login configurations
    login.login_view = 'login'
    login.login_message = 'You need to login to make purchases'
    login.login_message_category = 'warning'

    with app.app_context():
        from app.blueprints.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.blueprints.shop import bp as shop_bp
        app.register_blueprint(shop_bp)

        from app.blueprints.users import bp as user_bp
        app.register_blueprint(user_bp)

        from app.contexts.cart import cart_context
        
        from app.blueprints.main import errors      
        

    return app

