from functools import wraps
from flask import request, jsonify

from app.models import User 
# here we are creating the @token_required decorator for protecting our API resources


def token_required(func): # takes in a callback function
    @wraps(func)
    def decorated(*args, **kwargs): # letting our function accept an infinite number of things
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return {
                'status': 'not ok',
                'message': "Missing Header. Please add the 'x-access-token' to your headers"
            }
        if not token:
            return {
                'status': 'not ok',
                'message': "Missing Auth Token. Please log in with a username that has a valid token."
            }
        user = User.query.filter_by(apitoken=token) # finding the user that the token belongs to
        if not user: # if they don't havea a valid token
            return {
                'status': 'not ok',
                'message': 'That token does not belong to a valid user.'
            }
        return func(*args, **kwargs)
    return decorated