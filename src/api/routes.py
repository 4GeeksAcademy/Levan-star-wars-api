from api.models import db, User, Planet, People, Favorite
from flask import  request, jsonify, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Endpoint to create a new user or retrieve all users
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api.route('/users', methods=['GET', 'POST','DELETE'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
             error_response = {
            "error": " not found"
        }
             return jsonify(error_response), 404
        if 'email' not in data:
             error_response = {
            "error": "email not found"
        }
             return jsonify(error_response), 404
        if 'password' not in data:
            error_response = {
            "error": "Password not found"
        }
            return jsonify(error_response), 404
        if 'is_active' not in data:
            is_active = True
        else:
            is_active = data['is_active']
        user = User(email=data['email'], password=data['password'], is_active=is_active)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 201
@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        error_response = {
            "error": "User not found"
        }
        return jsonify(error_response), 404
    favorites_to_delete = Favorite.query.filter_by(user_id=user_id).all()
    for favorite in favorites_to_delete:
        db.session.delete(favorite)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User  {user_id} and all favorites have been deleted."}), 200

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22
# Endpoint to retrieve favorites of a user if they exist
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    current_user = User.query.filter_by(id=user_id).first()
    if current_user is None:
        error_response = {
            "error": "User not found"
        }
        return jsonify(error_response), 404
    favorites = current_user.favorites
    return jsonify([favorite.serialize() for favorite in favorites]), 200
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Endpoint to create a new person from Star Wars or retrieve all people from Star Wars
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == 'GET':
        people = People.query.all()
        return jsonify([p.serialize() for p in people]), 200
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            raise APIException('No data provided', status_code=400)
        name = data.get('name')
        gender = data.get('gender')
        height = data.get('height')
        mass = data.get('mass')
        homeworld = data.get('homeworld')
        if not name or not gender or not height or not mass or not homeworld:
            raise APIException('Missing required parameters', status_code=400)
        people = People(name=name, gender=gender, height=height, mass=mass, homeworld=homeworld)
        db.session.add(people)
        db.session.commit()
        return jsonify(people.serialize()), 201
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#WE GET A SINGLE PEOPLE OF THE STARWARS 
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@api.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    people = People.query.get(people_id)
    if not people:
        error_response = {
            "error": "People not found"
        }
        return jsonify(error_response), 404
    return jsonify(people.serialize()), 200
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#WE GET ALL THE PEOPLE OF STARWARS OR CREATE ANOTHER PEOPLE
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api.route('/planets', methods=['GET', 'POST'])
def planets():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            raise APIException('No data provided', status_code=400)
        name = data.get('name')
        climate = data.get('climate')
        terrain = data.get('terrain')
        population = data.get('population')
        if not name or not climate or not terrain or not population:
            raise APIException('Missing required parameters', status_code=400)
        planet = Planet(name=name, climate=climate, terrain=terrain, population=population)
        db.session.add(planet)
        db.session.commit()
        return jsonify(planet.serialize()), 201
    elif request.method == 'GET':
        planets = Planet.query.all()
        return jsonify([p.serialize() for p in planets]), 200
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#HERE WE GET A SINGLE PLANET BASED ON THE PLANET'S ID
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        error_response = {
            "error": "Planet not found"
        }
        return jsonify(error_response), 404
    return jsonify(people.serialize()), 200


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Define endpoint for adding favorite planet or delete one
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def favorite_planet(planet_id):
    if request.method == 'POST':
        user_id = request.json['user_id']
        favorite_planet = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if favorite_planet:
            return jsonify({'message': f'Planet {planet_id} is already a favorite for user {user_id}.'}), 400
        else:
            favorite = Favorite(user_id=user_id, planet_id=planet_id)
            db.session.add(favorite)
            db.session.commit()
            return jsonify({'message': f'Added planet {planet_id} to favorites for user {user_id}.'})
    elif request.method == 'DELETE':
        user_id = request.json['user_id']
        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'message': f'Removed planet {planet_id} from favorites for user {user_id}.'})
        else:
            return jsonify({'message': f'Favorite planet {planet_id} not found for user {user_id}.'}), 404

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#Define endpoint for adding favorite people or delete one
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api.route('/favorite/people/<int:people_id>', methods=['POST','DELETE'])
def add_favorite_people(people_id):
    if request.method == 'POST':
        user_id = request.json['user_id']
        favorite_people = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if favorite_people:
            return jsonify({'message': f'People {people_id} is already a favorite for user {user_id}.'}), 400
        else:
            favorite = Favorite(user_id=user_id, people_id=people_id)
            db.session.add(favorite)
            db.session.commit()
            return jsonify({'message': f'Added people {people_id} to favorites for user {user_id}.'})
    elif request.method == 'DELETE':
        user_id = request.json['user_id']
        favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'message': f'Removed people {people_id} from favorites for user {user_id}.'})
        else:
            return jsonify({'message': f'Favorite people {people_id} not found for user {user_id}.'}), 404

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


if __name__ == '__main__':
    api.run(debug=True)