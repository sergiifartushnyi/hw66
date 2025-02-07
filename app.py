from flask import Flask
from database import db, init_db
from hw66.routes.user_routes import user_bp
from hw66.routes import item_bp
from hw66.routes.leaser_routes import leaser_bp
from hw66.routes.contract_routes import contract_bp
from hw66.routes.search_routes import search_bp
from hw66.routes.other_routes import other_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)

app.register_blueprint(user_bp)
app.register_blueprint(item_bp)
app.register_blueprint(leaser_bp)
app.register_blueprint(contract_bp)
app.register_blueprint(search_bp)
app.register_blueprint(other_bp)

if __name__ == '__main__':
    app.run(debug=True)