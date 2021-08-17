from flask import *
app = Flask(__name__)
app.debug = True
app.secret_key = 'secret_key'
from server.routes import *

