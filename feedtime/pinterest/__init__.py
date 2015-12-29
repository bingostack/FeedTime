from flask import Blueprint

pinterest = Blueprint('pinterest', __name__, template_folder='templates', static_folder='static')

import pinterest
