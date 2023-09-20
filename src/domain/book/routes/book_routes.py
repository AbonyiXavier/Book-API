from flask import Blueprint, request, jsonify, make_response
from src.common.constant import API_PREFIX_URL, BOOK_NOT_FOUND_MESSAGE, PAGINATION_ARGS, STATUS_CODES
from src.domain.book.models.book_model import Book, Currency
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db

# Create a Blueprint for book_routes
book_routes = Blueprint("book_routes", __name__)

"""
  Get all books with pagination
  >>> page, per_page
  >>> endpoint : /books?page=2&per_page=10
"""

@book_routes.route(f"{API_PREFIX_URL}/book", methods=["GET"])
@jwt_required()
def get_books():
    try:
        # Get pagination parameters from query parameters
        page = int(request.args.get("page", PAGINATION_ARGS["page"]))
        per_page = int(request.args.get("per_page", PAGINATION_ARGS["per_page"]))
        max_per_page = int(
            request.args.get("max_per_page", PAGINATION_ARGS["max_per_page"])
        )

        # Ensure per_page is not greater than max_per_page
        per_page = min(per_page, max_per_page)

        # Calculate offset based on page and per_page
        offset = (page - 1) * per_page

        # Query for books with pagination
        books = Book.query.offset(offset).limit(per_page).all()

        # Calculate total number of books (for pagination headers)
        total_books = Book.query.count()

        # Calculate has_prev and has_next flags
        has_prev_page = page > 1
        has_next_page = offset + per_page < total_books

        # Prepare response data
        book_data = [book.json() for book in books]
        response_data = {
            "books": book_data,
            "page": page,
            "per_page": per_page,
            "total_books": total_books,
            "has_prev_page": has_prev_page,
            "has_next_page": has_next_page,
        }
        return make_response(
            jsonify({"message": "Books fetched successfully!", "data": response_data}),
            STATUS_CODES["ok"],
        )
    except Exception as e:
        error_message = f"Error fetching books: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )


"""
  Create book signup
  >>> title, author, isbn, price
"""

@book_routes.route(f"{API_PREFIX_URL}/book", methods=["POST"])
@jwt_required()
def create_book():
    try:
        title = request.json["title"]
        author = request.json["author"]
        isbn = request.json["isbn"]
        price = request.json["price"]

        # Check if 'currency' is provided in the request JSON
        if "currency" in request.json:
            currency = request.json["currency"]
        else:
            # Set the default currency to 'KR'
            currency = Currency.KR    

        title_exists = Book.query.filter_by(title=title).first()

        if title_exists:
            return make_response(
                jsonify({"message": "Book title already exists"}), STATUS_CODES["conflict"]
            )
        
        isbn_exists = Book.query.filter_by(isbn=isbn).first()

        if isbn_exists:
            return make_response(
                jsonify({"message": "Book isbn number already exists"}), STATUS_CODES["conflict"]
            )
        
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            price=price,
            currency=currency
        )
        db.session.add(book)
        db.session.commit()

        return make_response(
            jsonify(
                {
                    "message": "Your book has been created!",
                    "data": book.json(),
                }
            ),
            STATUS_CODES["created"],
        )
    except Exception as e:
        error_message = f"Error creating book: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )
   

"""
  Get book by id 
"""

@book_routes.route(f"{API_PREFIX_URL}/book/<string:id>", methods=["GET"])
@jwt_required()
def get_book(id):
    try:
        book = validate_and_get_book_by(id)

        if book is None:
            return make_response(
                jsonify({"message": BOOK_NOT_FOUND_MESSAGE}), STATUS_CODES["not_found"]
            )
        
        return make_response(
            jsonify({"message": "Book fetched successfully!", "data": book.json()}),
            STATUS_CODES["ok"],
        )
    except Exception as e:
        error_message = f"Error fetching book: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )
    

"""
  Delete book by id 
"""   

@book_routes.route(f"{API_PREFIX_URL}/book/<string:id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    try:
        book = validate_and_get_book_by(id)

        if book is None:
            return make_response(
                jsonify({"message": BOOK_NOT_FOUND_MESSAGE}), STATUS_CODES["not_found"]
            )
        
        db.session.delete(book)
        db.session.commit()

        return make_response(
            jsonify({"message": "Book deleted successfully!", "data": book.json()}),
            STATUS_CODES["ok"],
        )
    except Exception as e:
        error_message = f"Error deleting book: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )
    


"""
  update book by id 
"""   

@book_routes.route(f"{API_PREFIX_URL}/book/<string:id>", methods=["PATCH"])
@jwt_required()
def update_book(id):
    try:
        if not request.json:
            return make_response(
                jsonify({"message": "input field(s) required"}), STATUS_CODES["bad_request"]
            )
        
        book = validate_and_get_book_by(id)

        if book is None:
            return make_response(
                jsonify({"message": BOOK_NOT_FOUND_MESSAGE}), STATUS_CODES["not_found"]
            )
        
        book.title = request.json.get('title', book.title)
        book.author = request.json.get('author', book.author)
        book.isbn = request.json.get('isbn', book.isbn)
        book.price = request.json.get('price', book.price)
        book.currency = request.json.get('currency', book.currency)
        db.session.commit()

        return make_response(
            jsonify({"message": "Book updated successfully!", "data": book.json()}),
            STATUS_CODES["ok"],
        )
    except Exception as e:
        error_message = f"Error updating book: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )
    


def validate_and_get_book_by(id):
    book = Book.query.get(id)

    if not book:
        return None
        
    return book