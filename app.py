from flask import Flask
from config import SECRET_KEY
from routes.main import main_bp
from routes.messages import messages_bp
from routes.api import api_bp
from routes.static_files import static_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY


app.register_blueprint(main_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(api_bp)
app.register_blueprint(static_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
