# Define API endpoints using a nested dictionary structure
API_ENDPOINTS = {
    "BASE_URL": "/api/v1",
    "USERS": {
        "BASE_URL": "/users",
        "REGISTER": "/register",
        "LOGIN": "/login",
        "WHO_AM_I": "/whoami",
        "USER_BY_ID": "/{userId}",
        "GET_ALL_USERS": "/",
    },
    "PROJECT": {
        "BASE_URL": "/projects",
    },
}
ALLOWED_IMAGES_TYPE = ["image/jpeg", "image/jpg", "image/png"]
MAX_FILE_UPLOAD_SIZE = 2097152

# Docstring for API_ENDPOINTS
"""
API_ENDPOINTS: Dictionary containing the structure of API endpoints.

Structure:
{
    "BASE_URL": "/api/v1",
    "USERS": {
        "BASE_URL": "/users",
        "REGISTER": "/register",
        "LOGIN": "/login",
        "WHO_AM_I": "/whoami",
        "USER_BY_ID": "/{userId}",
        "GET_ALL_USERS": "/"
    },
    "PROJECT": {
        "BASE_URL": "/projects",
    },
}
"""

# Comments for clarity
"""
- 'BASE_URL': The base URL for the entire API.
- 'USERS': Endpoints related to user operations.
    - 'BASE_URL': Base URL for user-related endpoints.
    - 'REGISTER': User registration endpoint.
    - 'LOGIN': User login endpoint.
    - 'WHO_AM_I': Endpoint to get information about the currently logged-in user.
    - 'USER_BY_ID': Endpoint to retrieve a user by ID.
    - 'GET_ALL_USERS': Endpoint to get all users.
- 'PROJECT': Endpoints related to project operations.
    - 'BASE_URL': Base URL for project-related endpoints.
"""

# Note: The variable name 'API_ENDPOINTS' is kept as is, as it is a common convention to use uppercase for constants.
