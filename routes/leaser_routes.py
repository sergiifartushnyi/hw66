from flask import Blueprint, jsonify
from hw66.app import Leaser

leaser_bp = Blueprint('leaser', __name__)

@leaser_bp.route('/leasers', methods=['GET'])
def leasers():
    leasers = Leaser.query.all()
    return jsonify([{'id': leaser.id, 'name': leaser.name} for leaser in leasers]), 200

@leaser_bp.route('/leasers/<int:leaser_id>', methods=['GET'])
def leaser_detail(leaser_id):
    leaser = Leaser.query.get(leaser_id)
    if not leaser:
        return jsonify({'message': 'Leaser not found'}), 404
    return jsonify({'id': leaser.id, 'name': leaser.name}), 200