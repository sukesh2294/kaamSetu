from app import create_app
from flask import render_template
from app.extensions import db

app = create_app()
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

