import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import setup_db, Paint
from auth.auth import AuthError, requires_auth

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
# Access the JWT_SECRET environment variable
jwt_secret = os.getenv('JWT_SECRET')

@app.route('/')
def home():
    return f"JWT Secret is: {jwt_secret}"
	
'''
implement endpoint
    GET /paints
        it should be a public endpoint
        it should contain only the paint.short() data representation
    returns status code 200 and json {"success": True, "paints": paints} where paints is the list of paints
        or appropriate status code indicating reason for failure
'''
@app.route('/paints', methods=['GET'])
@requires_auth('get:paints')
def get_paints():
    try:
        # Get the short representation of each paint
        paints_short = [paint.short() for paint in paints]
        return jsonify({
            "success": True,
            "paints": paints_short
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

'''
implement endpoint
    GET /paints-detail
        it should require the 'get:paints-detail' permission
        it should contain the paint.long() data representation
    returns status code 200 and json {"success": True, "paints": paints} where paints is the list of paints
        or appropriate status code indicating reason for failure
'''
@app.route('/paints-detail', methods=['GET'])
@requires_auth('get:paints-detail')
def get_paints_detail(payload):
    try:
        # Get the long representation of each paint
        paints_long = [paint.long() for paint in paints]
        return jsonify({
            "success": True,
            "paints": paints_long
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

'''
implement endpoint
    POST /paints
        it should create a new row in the paints table
        it should require the 'post:paints' permission
        it should contain the paint.long() data representation
    returns status code 200 and json {"success": True, "paints": paint} where paint an array containing only the newly created paint
        or appropriate status code indicating reason for failure
'''
@app.route('/paints', methods=['POST'])
@requires_auth('post:paints')
def create_paint(payload):
    try:
        data = request.get_json()
        new_paint = Paint(id=len(paints) + 1, title=data['title'], recipe=data['recipe'])
        paints.append(new_paint)
        return jsonify({
            "success": True,
            "paints": [new_paint.long()]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

'''
implement endpoint
    PATCH /paints/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:paints' permission
        it should contain the paint.long() data representation
    returns status code 200 and json {"success": True, "paints": paint} where paint an array containing only the updated paint
        or appropriate status code indicating reason for failure
'''
@app.route('/paints/<int:id>', methods=['PATCH'])
@requires_auth('patch:paints')
def update_paint(payload, id):
    try:
        paint = next((d for d in paints if d.id == id), None)
        if not paint:
            return jsonify({"success": False, "error": 404, "message": "Paint not found"}), 404

        data = request.get_json()
        if 'title' in data:
            paint.title = data['title']
        if 'recipe' in data:
            paint.recipe = data['recipe']

        return jsonify({
            "success": True,
            "paints": [paint.long()]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

'''
implement endpoint
    DELETE /paints/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:paints' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/paints/<int:id>', methods=['DELETE'])
@requires_auth('delete:paints')
def delete_paint(payload, id):
    try:
        paint = next((d for d in paints if d.id == id), None)
        if not paint:
            return jsonify({"success": False, "error": 404, "message": "Paint not found"}), 404

        paints.remove(paint)
        return jsonify({
            "success": True,
            "delete": id
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
implement error handler for AuthError error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_auth_error(error):
    response = jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    })
    response.status_code = error.status_code
    return response
