from models import db
from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()
    print(" All tables created successfully.")
