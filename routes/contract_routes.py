from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from hw66.models import Contract, Item
from database import db

contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/contracts')
@login_required
def contracts():
    contracts = Contract.query.filter_by(leaser_id=current_user.id).all()
    return render_template('contracts.html', contracts=contracts)

@contract_bp.route('/contract_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def contract_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        terms = request.form['terms']
        new_contract = Contract(item_id=item.id, leaser_id=current_user.id, terms=terms)
        item.status = 'contracted'
        db.session.add(new_contract)
        db.session.commit()
        return redirect(url_for('contract.contracts'))
    return render_template('contract_item.html', item=item)