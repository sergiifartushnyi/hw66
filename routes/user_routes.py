from flask import Blueprint, request, session, jsonify
from hw66 import db
from hw66 import User, Favourite, SearchHistory

user_bp = Blueprint('user', __name__)

def get_user_from_session():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 400
    return 'Login Form'

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    return 'Registration Form'

@user_bp.route('/logout', methods=['POST', 'DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@user_bp.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile():
    user = get_user_from_session()
    if not user:
        return jsonify({'message': 'Not logged in'}), 401
    if request.method == 'GET':
        return jsonify({'username': user.username}), 200
    elif request.method in ['PUT', 'PATCH']:
        user.username = request.form.get('username', user.username)
        user.password = request.form.get('password', user.password)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Profile deleted successfully'}), 200

@user_bp.route('/profile/favourites', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def favourites():
    user = get_user_from_session()
    if not user:
        return jsonify({'message': 'Not logged in'}), 401
    if request.method == 'GET':
        favourites = Favourite.query.filter_by(user_id=user.id).all()
        return jsonify([{'id': fav.id, 'item_id': fav.item_id} for fav in favourites]), 200
    elif request.method == 'POST':
        item_id = request.form['item_id']
        new_favourite = Favourite(user_id=user.id, item_id=item_id)
        db.session.add(new_favourite)
        db.session.commit()
        return jsonify({'message': 'Favourite added successfully'}), 201
    elif request.method in ['DELETE', 'PATCH']:
        favourite_id = request.form['favourite_id']
        favourite = Favourite.query.filter_by(id=favourite_id, user_id=user.id).first()
        if not favourite:
            return jsonify({'message': 'Favourite not found'}), 404
        if request.method == 'DELETE':
            db.session.delete(favourite)
            db.session.commit()
            return jsonify({'message': 'Favourite deleted successfully'}), 200
        elif request.method == 'PATCH':
            favourite.item_id = request.form.get('item_id', favourite.item_id)
            db.session.commit()
            return jsonify({'message': 'Favourite updated successfully'}), 200

@user_bp.route('/profile/favourites/<int:favourite_id>', methods=['DELETE'])
def delete_favourite(favourite_id):
    user = get_user_from_session()
    if not user:
        return jsonify({'message': 'Not logged in'}), 401
    favourite = Favourite.query.filter_by(id=favourite_id, user_id=user.id).first()
    if not favourite:
        return jsonify({'message': 'Favourite not found'}), 404
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({'message': 'Favourite deleted successfully'}), 200

@user_bp.route('/profile/search_history', methods=['GET', 'DELETE'])
def search_history():
    user = get_user_from_session()
    if not user:
        return jsonify({'message': 'Not logged in'}), 401
    if request.method == 'GET':
        search_history = SearchHistory.query.filter_by(user_id=user.id).all()
        return jsonify([{'id': history.id, 'search_query': history.search_query} for history in search_history]), 200
    elif request.method == 'DELETE':
        SearchHistory.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        return jsonify({'message': 'Search history deleted successfully'}), 200