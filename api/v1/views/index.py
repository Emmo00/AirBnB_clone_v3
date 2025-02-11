#!/usr/bin/python3
''' Defines routes '''
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    ''' returns status in JSON '''
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    ''' Retrieves the number of each object by type '''
    return jsonify({'amenities': storage.count(Amenity),
                    'cities': storage.count(City),
                    'places': storage.count(Place),
                    'reviews': storage.count(Review),
                    'states': storage.count(State),
                    'users': storage.count(User)})
