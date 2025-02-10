from flask import Blueprint

item_bp = Blueprint('item', __name__)

# Додайте свої маршрути тут
@item_bp.route('/items')
def get_items():
    return "Here are the items"