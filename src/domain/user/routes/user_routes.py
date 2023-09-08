from flask import Flask, Blueprint, request, jsonify, make_response
from common.constant import PAGINATION_ARGS, STATUS_CODES
from domain.user.models.user_model import User
from flask_bcrypt import Bcrypt
from domain.user.models.user_model import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
import uuid


app = Flask(__name__)
bcrypt = Bcrypt(app)

# Set up a list to store revoked tokens
revoked_tokens = set()

# Create a Blueprint for user_routes
user_routes = Blueprint("user_routes", __name__)

"""
  Get all users with pagination
  >>> page, per_page
  >>> endpoint : /users?page=2&per_page=10
"""

@user_routes.route("/users", methods=["GET"])
@jwt_required()
def get_users():
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

        # Query for users with pagination
        users = User.query.offset(offset).limit(per_page).all()

        # Calculate total number of users (for pagination headers)
        total_users = User.query.count()

        # Calculate has_prev and has_next flags
        has_prev_page = page > 1
        has_next_page = offset + per_page < total_users

        # Prepare response data
        user_data = [user.json() for user in users]
        response_data = {
            "users": user_data,
            "page": page,
            "per_page": per_page,
            "total_users": total_users,
            "has_prev_page": has_prev_page,
            "has_next_page": has_next_page,
        }
        return make_response(
            jsonify({"message": "Users fetched successfully!", "data": response_data}),
            STATUS_CODES["ok"],
        )
    except Exception as e:
        error_message = f"Error fetching users: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )


"""
  User signup
  >>> first_name, last_name, email, password
"""


@user_routes.route("/signup", methods=["POST"])
def signup():
    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]
        password = request.json["password"]

        user_exists = User.query.filter_by(email=email).first()

        if user_exists:
            return make_response(
                jsonify({"error": "Email already exists"}), STATUS_CODES["conflict"]
            )

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Generate a unique jti
        jti = str(uuid.uuid4())

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            jti=jti,
        )
        db.session.add(user)
        db.session.commit()

        user_dict = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        access_token = create_access_token(identity=user_dict)

        return make_response(
            jsonify(
                {
                    "message": "Your account has been created!",
                    "data": user_dict,
                    "access_token": access_token,
                }
            ),
            STATUS_CODES["created"],
        )
    except Exception as e:
        error_message = f"Error signing up user: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )


"""
 User Login
 >>> email, password
"""

@user_routes.route("/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return make_response(
                jsonify({"error": "invalid credentials provided"}),
                STATUS_CODES["un_authorized"],
            )

        password_match = bcrypt.check_password_hash(user.password, password)

        if not password_match:
            return make_response(
                jsonify({"error": "invalid credentials provided"}),
                STATUS_CODES["un_authorized"],
            )

        if user and password_match:
            user_dict = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }

            access_token = create_access_token(identity=user_dict)

            return make_response(
                jsonify(
                    {
                        "message": "Login successful!",
                        "data": user_dict,
                        "access_token": access_token,
                    }
                ),
                STATUS_CODES["ok"],
            )
    except Exception as e:
        error_message = f"Error logging in user: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )


'''
    User Logout
'''

@user_routes.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
         # Get the current user's identity
        current_user = get_jwt_identity()
        user_id = current_user.get("id")

        # Generate a unique jti for this logout event
        jti = str(uuid.uuid4())

        # Add the jti to the revoked tokens list
        revoked_tokens.add(jti)

        # Optionally, you can save the jti to the user model as well
        user = User.query.filter_by(id=user_id).first()
        user.jti = jti
        db.session.commit()

        return make_response(
            jsonify({"message": "Logout successful"}), STATUS_CODES["ok"]
        )
    except Exception as e:
        error_message = f"Error logging out user: {str(e)}"
        return make_response(
            jsonify({"message": error_message}), STATUS_CODES["internal_server_error"]
        )
