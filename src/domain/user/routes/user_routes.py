from flask import Flask, Blueprint, request, jsonify, make_response
from domain.user.models.user_model import User


app = Flask(__name__)

# Create a Blueprint for user_routes
user_routes = Blueprint('user_routes', __name__)

# get all users
@user_routes.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except Exception as e:
    error_message = f'Error fetching users: {str(e)}'
    return make_response(jsonify({'message': error_message}), 500)