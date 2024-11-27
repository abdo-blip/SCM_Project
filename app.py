from flask import Flask
from models import db
from auth import auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

print(app.url_map)
db.init_app(app)


app.register_blueprint(auth, url_prefix='/auth')


with app.app_context():
    db.create_all()


@app.route('/welcome', methods=['GET'])
def welcome():
    return "Welcome to my Application!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

