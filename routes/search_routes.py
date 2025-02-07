from flask import Blueprint, request, jsonify
from hw66.database import db
from hw66.app import Item, SearchHistory
from hw66.routes.user_routes import get_user_from_session

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        query = request.args.get('query')
        results = Item.query.filter(Item.name.contains(query)).all()
        return jsonify([{'id': item.id, 'name': item.name, 'leaser_id': item.leaser_id} for item in results]), 200
    elif request.method == 'POST':
        query = request.form['query']
        user = get_user_from_session()
        if user:
            new_search = SearchHistory(user_id=user.id, search_query=query)
            db.session.add(new_search)
            db.session.commit()
        results = Item.query.filter(Item.name.contains(query)).all()
        return jsonify([{'id': item.id, 'name': item.name, 'leaser_id': item.leaser_id} for item in results]), 200