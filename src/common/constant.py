PAGINATION_ARGS = {
    'page': 1,  # Default page 1 if not specified
    'per_page': 10, # Default per_page 10 if not specified
    'max_per_page': 100 # Default max_per_page 100 if not specified
}

STATUS_CODES = {
    'created': 201,
    'ok': 200,
    'bad_request': 400,
    'conflict': 409,
    'not_found': 404,
    'un_authorized': 401,
    'internal_server_error': 500,
}

API_PREFIX_URL = '/api/v1'

BOOK_NOT_FOUND_MESSAGE = 'Book not found'