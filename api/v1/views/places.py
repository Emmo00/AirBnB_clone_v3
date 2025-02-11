#!/usr/bin/python3
''' This module defines view for the Place object '''
from api.v1.views import place_views
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from flask import request, abort, jsonify


@place_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    ''' Retrives all Place objects of a City '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@place_views.route('/places/<place_id>')
def get_place(place_id):
    ''' Retrieves a place object '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@place_views.route('/places/<place_id>',
                   methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    ''' Deletes a place '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@place_views.route('/cities/<city_id>/places',
                   methods=['POST'], strict_slashes=False)
def post_place(city_id):
    ''' Creates a place '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    else:
        if 'user_id' not in data:
            abort(400, description='Missing user_id')
        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)
        if 'name' not in data:
            abort(400, description='Missing name')
        place = Place(**data)
        place.city_id = city.id
        place.save()
        return jsonify(place.to_dict()), 201


@place_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    ''' Updates a place '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    else:
        for key, value in data.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                continue
            setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@place_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    ''' Retrieves all Place objects depending on the data body '''
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    all_places = list(storage.all(Place).values())
    city_ids = []
    if 'cities' in data:
        city_ids.extend(data['cities'])
    if 'states' in data:
        for state_id in data['states']:
            state = storage.get(State, state_id)
            if state:
                city_ids.extend([city.id for city in state.cities])
    for index, place in reversed(list(enumerate(all_places))):
        if len(city_ids) > 0 and place.city_id not in city_ids:
            all_places.pop(index)
    if 'amenities' in data:
        for index, place in reversed(list(enumerate(all_places))):
            has_amenity = False
            for amenity in place.amenities:
                if amenity in data['amenities']:
                    has_amenity = True
                    break
            if not has_amenity:
                all_places.pop(index)
    return jsonify([place.to_dict() for place in all_places])
