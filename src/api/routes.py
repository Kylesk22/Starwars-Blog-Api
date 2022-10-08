"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Person, Planet, Favorites
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# user routes
@api.route('/user', methods=['POST'])
def create_user():
    request_body = request.get_json()
    new_user = User(
        email = request_body['email'],
        password = request_body['password'],
        is_active = True
        )

    db.session.add(new_user)
    db.session.commit()

    return f"A new user has been created"

@api.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    user_list = list(map(lambda x: x.serialize(), all_users))
    return jsonify(user_list), 200

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    selected_user = User.query.get(user_id)
    this_user = selected_user.serialize()
    return jsonify(this_user)
   




#people routes
@api.route('/people', methods=['GET', 'POST'])
def get_allPeople():
    if request.method =="GET":
        all_people = Person.query.all()
        all_people_list = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people_list), 200
    if request.method =="POST":
        request_body = request.get_json()
        new_person = Person(
            name = request_body['name'],
            height = request_body['height'],
            mass = request_body['mass'],
            hair_color = request_body['hair_color'],
            skin_color = request_body['skin_color'],
            gender = request_body['gender']            
            )

        db.session.add(new_person)
        db.session.commit()

        return f"A new person has been created"
        

@api.route('/people/<int:person_id>', methods=['GET', 'PUT'])
def get_person(person_id):
    if request.method == 'GET':
        selected_person = Person.query.get(person_id)
        this_person = selected_person.serialize()
        return jsonify(this_person)
    if request.method == 'PUT':
        selected_person = Person.query.get(person_id)
        request_body = request.get_json()
        if selected_person is None:
            raise APIException("Person not found", status_code=405)
        if "name" in request_body:
            selected_person.name = request_body['name']
        if "height" in request_body:
            selected_person.height = request_body['height']
        if "mass" in request_body:
            selected_person.mass = request_body['mass']
        if "hair_color" in request_body:
            selected_person.hair_color = request_body['hair_color']
        if "skin_color" in request_body:
            selected_person.skin_color = request_body['skin_color']
        if "gender" in request_body:
            selected_person.gender = request_body['gender']
        if "fav_person" in request_body:
            selected_person.fav_person += request_body['fav_person']
        if "fav_planet" in request_body:
            selected_person.fav_planet += request_body['fav_planet']
        
        db.session.commit()
        
        return jsonify(selected_person.serialize()), 200

# planet routes
@api.route('/planets', methods=['GET', 'POST'])
def get_allPlanets():
    if request.method =="GET":
        all_planets = Planet.query.all()
        all_planets_list = list(map(lambda x: x.serialize(), all_planets))
        return jsonify(all_planets_list), 200
    if request.method =="POST":
        request_body = request.get_json()
        new_planet = Planet(
            name = request_body['name'],
            population = request_body['population'],
            terrain = request_body['terrain'],         
            )

        db.session.add(new_planet)
        db.session.commit()

        return f"A new planet has been created"
        

@api.route('/planets/<int:planet_id>', methods=['GET', 'PUT'])
def get_planet(planet_id):
    if request.method == 'GET':
        selected_planet = Planet.query.get(planet_id)
        this_planet = selected_planet.serialize()
        return jsonify(this_planet)
    if request.method == 'PUT':
        selected_planet = Planet.query.get(planet_id)
        request_body = request.get_json()
        if selected_planet is None:
            raise APIException("Planet not found", status_code=405)
        if "name" in request_body:
            selected_planet.name = request_body['name']
        if "population" in request_body:
            selected_planet.population = request_body['population']
        if "terrain" in request_body:
            selected_planet.terrain = request_body['terrain']

        
        db.session.commit()
        
        return jsonify(selected_planet.serialize()), 200


# favorite routes
@api.route('/user/favorites', methods=['POST'])
def post_favorites():
    request_body = request.get_json()
    user_id = request_body['user_id']
    person_id = request_body['person_id']
    planet_id  = request_body['planet_id']

    person_record = Favorites.query.filter_by(user_id=user_id, person_id=person_id).first()
    planet_record = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    print(person_record)
    print(planet_record)

    if person_record is None:
        person_record = Favorites(
            user_id = user_id,
            person_id = person_id,
        )
        db.session.add(person_record)
        db.session.commit()


    if planet_record is None:
        planet_record = Favorites(
            user_id = user_id,
            planet_id = planet_id
        )
        db.session.add(planet_record)
        db.session.commit()
        return( f"Added Successfully")
        
    else: 
        return f"Already in Favorites"

    

@api.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    selected_favorite = Favorites.query.filter_by(user_id= user_id)
    favorite_list = list(map(lambda x: x.serialize(), selected_favorite))
    
    return jsonify(favorite_list)


# Delete Methods

@api.route('/user/favorites/<int:user_id>', methods=['DELETE'])
def delete_favorites(user_id):
        try:
            selected_favorite = User.query.get(user_id).favorites
            list(map(lambda x: db.session.delete(x), selected_favorite))

            
            db.session.commit()
            
            return "Deleted"

        except NameError:
            
            print("ERROR")

@api.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorites(user_id, planet_id):
    fav = User.query.get(user_id).favorites

    fav_list = list(map(lambda x: db.session.delete(x) if x.planet_id == planet_id else print("Not Found"), fav))
    db.session.commit()
    return "Planet Deleted"

@api.route('/user/<int:user_id>/favorites/people/<int:person_id>', methods=['DELETE'])
def delete_person_favorites(user_id, person_id):
    fav = User.query.get(user_id).favorites

    fav_list = list(map(lambda x: db.session.delete(x) if x.person_id == person_id else print("Not Found"), fav))
    db.session.commit()
    return "Person Deleted"

    
        