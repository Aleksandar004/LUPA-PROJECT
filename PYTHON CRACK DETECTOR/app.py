from flask import Flask
from routes import process_crack_route

app = Flask(__name__)

app.register_blueprint(process_crack_route)

if __name__ == '__main__':
    app.run(debug=True)
