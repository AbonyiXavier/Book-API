
from app_factory import create_app
from src.domain.user.routes.user_routes import user_routes
from src.domain.book.routes.book_routes import book_routes

app = create_app()

# Register the user_routes blueprint
app.register_blueprint(user_routes)

# Register the book_routes blueprint
app.register_blueprint(book_routes)

@app.route("/")
def index():
    return 'Welcome API 👈👈👈'

if __name__ == '__main__':
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
    )
