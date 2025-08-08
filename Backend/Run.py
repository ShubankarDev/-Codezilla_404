from flask import Flask
from config import Config
from db import db
from routes_admin import admin_bp
from routes_worker import worker_bp
from routes_user import user_bp
from routes_home import home_bp
from routes_auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(worker_bp, url_prefix='/worker')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/auth')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
