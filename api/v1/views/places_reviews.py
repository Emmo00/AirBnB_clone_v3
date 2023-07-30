#!/usr/bin/python3
''' This module defines views for Review objects '''
from flask import request, abort, jsonify
from api.v1.views import review_views
from models import storage
from models.review import Review
from models.place import Place


@review_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    ''' Retrieves all reviews of a place '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return (jsonify(reviews))


@review_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    ''' Retrieves a review object '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@review_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    ''' Deletes a review '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@review_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    if 'text' not in data:
        abort(400, description='Missing text')
    review = Review(**data)
    review.place_id = place.id
    review.save()
    return jsonify(review.to_dict()), 201


@review_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    ''' Updates a review '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            continue
        setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200