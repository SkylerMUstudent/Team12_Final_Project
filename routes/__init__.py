from flask import Blueprint

# Create blueprint instances
main_bp = Blueprint('main', __name__, template_folder='templates')
admin_bp = Blueprint('admin', __name__, template_folder='templates')
reservation_bp = Blueprint('reservation', __name__, template_folder='templates')

# Import routes after blueprint creation to avoid circular imports
from . import main, admin, reservation
