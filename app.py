from flask import Flask
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
