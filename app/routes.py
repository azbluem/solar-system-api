from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app import db

planet_bp = Blueprint("planet_bp",__name__,url_prefix="/planets")


# planets = [Planet(1,"Mercury","It's solid",0),
#         Planet(2,"Mars","It's red",1000000),
#         Planet(3,"Earth","The blue marble",8000000000)]

@planet_bp.route("", methods=['POST'])
def make_planet():
    response_body = request.get_json()
    new_planet = Planet(
        name=response_body["name"],
        description=response_body["description"],
        population=response_body["population"]
    )

    db.session.add(new_planet)
    db.session.commit()

    return make_response(jsonify(f"Planet {new_planet.name} was created"),201)

@planet_bp.route('', methods=['GET'])
def get_all_planets():
    planet_list=[]
    planets = Planet.query.all()
    for planet in planets:
        planet_list.append({
            "id":planet.id,
            "name":planet.name,
            "description":planet.description,
            "population":planet.population
        })
    return jsonify(planet_list)

@planet_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return ({
            "id":planet.id,
            "name":planet.name,
            "description":planet.description,
            "population":planet.population
        })

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"Planet with ID {planet_id} invalid"}, 400))
    planet = Planet.query.get(planet_id)
    if not planet:
        abort(make_response({"message":f"Planet with ID {planet_id} not in solar system"}, 404))
    return planet

@planet_bp.route('/<planet_id>', methods=['DELETE'])
def blow_planet_up(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f'Planet with ID {planet.id} targetted by death star',202)