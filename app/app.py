from flask import Flask, render_template, LoginManager, User
from database import db, init_db
from hw66.routes import auth_bp, item_bp, contract_bp
from flask_login import LoginManage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(auth_bp)
app.register_blueprint(item_bp)
app.register_blueprint(contract_bp)

if __name__ == '__main__':
    app.run(debug=True)