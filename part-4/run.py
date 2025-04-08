from app import create_app, db
from flask_cors import CORS

app = create_app()

CORS(app, origins=["http://localhost:5500"], supports_credentials=True)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
