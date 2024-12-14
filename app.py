from flask import Flask
from flask_cors import CORS
from routes.profiles import profiles_bp
from routes.insights import insights_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Register blueprints
app.register_blueprint(profiles_bp, url_prefix="/api/profiles")
app.register_blueprint(insights_bp, url_prefix="/api/insights")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
