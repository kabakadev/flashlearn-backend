from config import app, db
from routes import auth_routes, flashcard_routes, deck_routes

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Welcome to FlashLearn API!"


if __name__ == "__main__":
    app.run(debug=True)
