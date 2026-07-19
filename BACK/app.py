import os

from flask import Flask
from flask_cors import CORS

# ===== IMPORTS ===== 

from routes.home import home_bp
from routes.summer import summer_bp
from routes.winter import winter_bp
from routes.spring import spring_bp
from routes.fall import fall_bp

# ===== CORS =====

app = Flask(__name__)
CORS(app)

# ===== BLUEPRINTS =====

app.register_blueprint(home_bp)
app.register_blueprint(summer_bp)
app.register_blueprint(winter_bp)
app.register_blueprint(spring_bp)
app.register_blueprint(fall_bp)

# --- CHECKING ---

@app.route("/")
def back_status():
    return "A TODO VAPOR"

# --- PORTA BACK ---
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5500))
    app.run(host="0.0.0.0", port=port, debug=False)