from werkzeug.exceptions import HTTPException


class UserAlreadyExistsError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


class AspectNotFoundError(HTTPException):
    pass


class JsonLdContextError(HTTPException):
    pass


custom_errors = {
    'UnauthorizedError': {
        'message': "Authentication is required",
        'status': 401,
    },
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'AspectNotFoundError': {
        'message': "Aspect not found.",
        'status': 404,
    },
    'JsonLdContextError': {
        'message': "Error in JSON-LD Context.",
        'status': 400,
    },
}
