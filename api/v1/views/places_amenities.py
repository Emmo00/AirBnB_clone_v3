#!/usr/bin/python3
''' Defines a view for the link btw Place and Amenity objects '''
from api.v1.views import places_amenities_views
from flask import jsonify, abort
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t


@places_amenities_views.route('/<place_id>/amenities',
                              strict_slashes=False)
def get_amenities_from_place(place_id):
    ''' Retrieves the list of Amenity objects of a Place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@places_amenities_views.route('/<place_id>/amenities/<amenity_id>',
                              methods=['DELETE'],
                              strict_slashes=False)
def delete_amenity_of_place(place_id, amenity_id):
    ''' Deletes Amenity object of a Place '''
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)

    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)

    amenity.delete()
    place.save()

    return jsonify({}), 200


@places_amenities_views.route('/<place_id>/amenities/<amenity_id>',
                              methods=['POST'],
                              strict_slashes=False)
def link_amenity_to_a_place(place_id, amenity_id):
    ''' Links an Amenity object to a Place object '''
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)

    place.save()
    return jsonify(amenity.to_dict()), 201
