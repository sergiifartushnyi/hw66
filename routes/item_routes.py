from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from hw66.models import Item
from database import db

item_bp = Blueprint('item', __name__)

@item_bp.route('/items')
@login_required
def items():
    items = Item.query.all()
    return render_template('items.html', items=items)

@item_bp.route('/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_item = Item(name=name, description=description, owner_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('item.items'))
    return render_template('add_item.html')

@item_bp.route('/items/delete/<int:item_id>')
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.owner_id != current_user.id:
        return redirect(url_for('item.items'))
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('item.items'))