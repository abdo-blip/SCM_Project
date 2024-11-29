from flask import Flask
from models import db
from auth import auth
from flask import Flask, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, start_http_server

app = Flask(__name__)

start_http_server(8000)
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests' ,['method', 'endpoint'])


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

print(app.url_map)
db.init_app(app)


app.register_blueprint(auth, url_prefix='/auth')


with app.app_context():
    db.create_all()


@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

@app.route('/metrics')
def metrics():
    from prometheus_client import generate_latest
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/welcome', methods=['GET'])
def welcome():
    return "Welcome to my Application!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

