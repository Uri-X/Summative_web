from flask import Flask, render_template
from backend.routes.trips import trips_bp
from backend.routes.zones import zones_bp

app = Flask(__name__)

app.register_blueprint(trips_bp)
app.register_blueprint(zones_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
