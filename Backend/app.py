from flask import Flask
from flask_login import LoginManager
from login_controller import main as main_blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, AllUsers
from seed_data import seed_data
from routes_worker import worker_bp
from routes_user import user_bp
from routes_home import home_bp
#from Backend.routes_auth import auth_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'its-a-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

app.register_blueprint(main_blueprint)
 
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return AllUsers.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = AllUsers(
            email="admin@example.com",
            user_id="admin",
            password=generate_password_hash('admin123'),
            role="admin"
        )
        user = AllUsers(
            email="user@example.com",
            user_id="user",
            password=generate_password_hash('user123'),
            role="user"
        )
        worker = AllUsers(
            email="worker@example.com",
            user_id="worker",
            password=generate_password_hash('worker'),
            role="worker"
        )
        
        db.session.add(admin)
        db.session.add(worker)
        db.session.add(user)
        db.session.commit() 
        seed_data()
    app.run(debug=True)

app.register_blueprint(home_bp)
app.register_blueprint(worker_bp, url_prefix='/worker')
app.register_blueprint(user_bp, url_prefix='/user')

