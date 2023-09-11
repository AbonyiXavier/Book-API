
from os import environ
from common.constant import API_PREFIX_URL
from index import create_app
from domain.user.routes.user_routes import user_routes
from domain.book.routes.book_routes import book_routes

app = create_app()

# Register the user_routes blueprint
app.register_blueprint(user_routes)

# Register the book_routes blueprint
app.register_blueprint(book_routes)

@app.route(f"{API_PREFIX_URL}/")
def index():
    return 'Welcome API 👈👈👈'

if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(debug=True, port=port)
