import os
from dotenv import load_dotenv
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from jose.exceptions import JWTError

# Load environment variables from .env file
load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('AUTH_AUDIENCE')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header

'''
implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError("Authorization header is expected", 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError("Authorization header must start with Bearer", 401)
    elif len(parts) == 1:
        raise AuthError("Token not found", 401)
    elif len(parts) > 2:
        raise AuthError("Authorization header must be Bearer token", 401)

    token = parts[1]
    return token

'''
implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:paint')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    """Checks if the permission is in the JWT payload"""
    if 'permissions' not in payload:
        raise AuthError("Permissions not included in JWT", 403)

    if permission not in payload['permissions']:
        raise AuthError("Permission not found", 403)

    return True

'''
implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    """Verifies and decodes a JWT token from Auth0"""
    # Get the public key from Auth0
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Choose our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError("Authorization malformed", 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            # Decode the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            return payload

        except JWTError:
            raise AuthError("Token is invalid", 401)

    raise AuthError("Unable to find appropriate key", 401)

'''
implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:paint')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(payload, *args, **kwargs)
            except AuthError as e:
                return jsonify({"success": False, "error": e.status_code, "message": e.error}), e.status_code
        return wrapper
    return requires_auth_decorator
