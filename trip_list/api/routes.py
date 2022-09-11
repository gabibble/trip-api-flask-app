from flask import Blueprint, request, jsonify 
from trip_list.models import db, Trip, trip_schema, trips_schema
from trip_list.helpers import token_required


api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/getdata')
@token_required
def getdata():
    return{'some': 'value'}

#TODO add db 

#create trip
@api.route('/create_trip', methods = ['POST'])
@token_required
def create_trip(current_user_token):
    trip_name = request.json['trip_name']
    city = request.json['city']
    state = request.json['state']
    country = request.json['country']
    people = request.json['people']
    accommodation = request.json['accommodation']
    trip_length = request.json['trip_length']
    trip_date = request.json['trip_date']
    user_token = current_user_token.token
    
    print(current_user_token.token)

    trip = Trip(trip_name, city, state, country, people, accommodation, trip_length, trip_date, user_token=user_token)

    db.session.add(trip)
    db.session.commit()

    response = trip_schema.dump(trip)
    return jsonify(response) 

#get 1 trip
@api.route('/get_trip/<id>', methods = ['GET'])
@token_required
def get_trip(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        trip = Trip.query.get(id)
        response = trip_schema.dump(trip)
        return jsonify(response)
    else: 
        return jsonify({'message': 'Token is Missining!'}), 401

#get all trips
@api.route('/get_trips', methods = ['GET'])
@token_required
def get_trips(current_user_token):
    owner = current_user_token.token
    trips = Trip.query.filter_by(user_token = owner).all()
    response = trips_schema.dump(trips)
    return jsonify(response)

#get update trips

@api.route('/update_trip/<id>', methods = ['POST', 'PUT'])
@token_required
def update_trip(current_user_token, id):

    trip = Trip.query.get(id)

    trip.trip_name = request.json['trip_name']
    trip.city = request.json['city']
    trip.state = request.json['state']
    trip.country = request.json['country']
    trip.people = request.json['people']
    trip.accommodation = request.json['accommodation']
    trip.trip_length = request.json['trip_length']
    trip.trip_date = request.json['trip_date']
    trip.user_token = current_user_token.token

    db.session.commit()
    response = trip_schema.dump(trip)
    return jsonify(response)


@api.route('/del_trip/<id>', methods = ['DELETE'])
@token_required
def delete_trip(current_user_token, id):
    trip = Trip.query.get(id)
    db.session.delete(trip)
    db.session.commit()
    response = trip_schema.dump(trip)
    return jsonify(response)