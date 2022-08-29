import os
from turtle import title
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
# from jose import jwt
# from functools import wraps
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES

#Get drinks route
@app.route('/drinks', methods=['GET'])
def get_drinks():

    try:
        drinks = Drink.query.order_by(Drink.id).all()

        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        }, 200)

    except:
        abort(401)


#Get drinks-detail route
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):

    try:
        drinks = Drink.query.order_by(Drink.id).all()

        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        }, 200)

    except:
        abort(404)


#Post/Create drinks route
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = json.dumps(body.get('recipe', None))

    try:
        create_drink = Drink(
            title=new_title,
            recipe=new_recipe
        )
        create_drink.insert()

        return jsonify({
            'success': True,
            'drinks': [create_drink.long()]
        })

    except:
        abort(422)

#Patch/Edit drinks route
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(jwt,drink_id):

    try:
        drink = Drink.query.get(drink_id)
        body = request.get_json()

        if drink is None:
            abort(404)
        
        if 'title' and 'recipe' in body:
            drink.title = body['title']
            drink.recipe = body['recipe']

        drink.update()
        

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }, 200)

    except:
        abort(422)

#Delete drinks route
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt,drink_id):

    try:
        drink = Drink.query.get(drink_id)

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }, 200)

    except:
        abort(422)

# Error Handling

#Error 422 handler
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


#Error 404 handler
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

#AuthorError handler
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
