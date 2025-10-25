from flask import Flask
from extensions import db
from models import Members, Checkin, Products
import config

app=  Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return "flask mySQL DB initialized successfully"

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)