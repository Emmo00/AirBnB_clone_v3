#!/usr/bin/python3
''' This module defines view for the Place object '''
from api.v1.views import place_views
from models import storage
from models.city import City
from models.place import Place
from models.state import State
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

    all_empty = True
    for list in data.values():
        if list:
            all_empty = False

    if all_empty:
        all_places = list(storage.all(Place).values())

    else:
        all_cities = []
        if data.get('states'):
            for state_id in data['states']:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        all_cities.append(city.id)

        if data.get('cities'):
            # handle duplicates if any
            all_cities = set(all_cities + data['cities'])

        all_places = [storage.get(Place, id) for id in all_cities]

        if data.get('amenities'):
            result = []
            for amenity_id in data['amenities']:
                for place in all_places:
                    for amenity in place.amenities:
                        if amenity_id == amenity.id:
                            result.append(place.to_dict())

            return jsonify(result)

    return jsonify([place.to_dict() for place in all_places])
