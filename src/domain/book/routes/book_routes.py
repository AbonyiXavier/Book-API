from flask import Blueprint, request, jsonify, make_response
from common.constant import PAGINATION_ARGS, STATUS_CODES
from domain.book.models.book_model import Book
from flask_jwt_extended import jwt_required, get_jwt_identity


# Create a Blueprint for book_routes
book_routes = Blueprint("book_routes", __name__)

"""
  Get all books with pagination
  >>> page, per_page
  >>> endpoint : /books?page=2&per_page=10
"""

@book_routes.route("/books", methods=["GET"])
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
