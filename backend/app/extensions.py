from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Shared extension instances — bound to the app in create_app()
db = SQLAlchemy()
cors = CORS()
