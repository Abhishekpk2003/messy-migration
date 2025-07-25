from flask import Flask
from routes.users import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

@app.route('/')
def home():
    return {"message": "User Management System is running"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
