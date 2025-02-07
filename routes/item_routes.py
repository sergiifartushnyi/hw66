from flask import Blueprint, request, jsonify
from hw66.database import db
from hw66.app import Item

item_bp = Blueprint('item', __name__)

@item_bp.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        items = Item.query.all()
        return jsonify([{'id': item.id, 'name': item.name, 'leaser_id': item.leaser_id} for item in items]), 200
    elif request.method == 'POST':
        name = request.form['name']
        leaser_id = request.form['leaser_id']
        new_item = Item(name=name, leaser_id=leaser_id)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item added successfully'}), 201

@item_bp.route('/items/<int:item_id>', methods=['GET', 'DELETE'])
def item_detail(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    if request.method == 'GET':
        return jsonify({'id': item.id, 'name': item.name, 'leaser_id': item.leaser_id}), 200
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}), 200