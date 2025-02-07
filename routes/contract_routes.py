from flask import Blueprint, request, jsonify
from hw66.database import db
from hw66.app import Contract

contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/contracts', methods=['GET', 'POST'])
def contracts():
    if request.method == 'GET':
        contracts = Contract.query.all()
        return jsonify([{'id': contract.id, 'item_id': contract.item_id, 'user_id': contract.user_id} for contract in contracts]), 200
    elif request.method == 'POST':
        item_id = request.form['item_id']
        user_id = request.form['user_id']
        new_contract = Contract(item_id=item_id, user_id=user_id)
        db.session.add(new_contract)
        db.session.commit()
        return jsonify({'message': 'Contract added successfully'}), 201

@contract_bp.route('/contracts/<int:contract_id>', methods=['GET', 'PATCH', 'PUT'])
def contract_detail(contract_id):
    contract = Contract.query.get(contract_id)
    if not contract:
        return jsonify({'message': 'Contract not found'}), 404
    if request.method == 'GET':
        return jsonify({'id': contract.id, 'item_id': contract.item_id, 'user_id': contract.user_id}), 200
    elif request.method in ['PATCH', 'PUT']:
        contract.item_id = request.form.get('item_id', contract.item_id)
        contract.user_id = request.form.get('user_id', contract.user_id)
        db.session.commit()
        return jsonify({'message': 'Contract updated successfully'}), 200