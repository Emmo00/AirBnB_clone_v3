#!/usr/bin/python3
''' This module defines views for the User object '''
from api.v1.views import user_views
from models import storage
from models.user import User
from flask import request, abort, jsonify


@user_views.route('/users', strict_slashes=False)
def get_users():
    ''' Retrives all user objects '''
    users = list(storage.all(User).values())
    json_rep = [user.to_dict() for user in users]
    return jsonify(json_rep)


@user_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    ''' Retrives a user object '''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())



@user_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    ''' Deletes a user '''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@user_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    ''' Adds a user '''
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    else:
        if 'email' not in data:
            abort(400, description='Missing email')
        if 'password' not in data:
            abort(400, description='Missing password')
        user = User(**data)
        user.save()
        return jsonify(user.to_dict()), 201


@user_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    ''' Updates a user '''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    else:
        for key, value in data.items():
            if key in ['id', 'email', 'created_at', 'updated_at']:
                continue
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
