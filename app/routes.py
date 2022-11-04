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
    name_query = request.args.get('name')
    description_query = request.args.get('description')
    population_query = request.args.get('population')
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    elif population_query:
        planets = Planet.query.filter(Planet.population>=population_query).all()
    elif description_query:
        planets = Planet.query.filter(Planet.description.contains(description_query)).all()
    else:
        planets = Planet.query.all()
    planet_list=[]
    for planet in planets:
        planet_list.append(planet.dictionfy())
    return make_response(jsonify(planet_list),200)

@planet_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return make_response(planet.dictionfy(),200)

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"Planet with ID {planet_id} invalid"}, 400))
    planet = Planet.query.get(planet_id)
    if not planet:
        abort(make_response({"message":f"Planet with ID {planet_id} not in solar system"}, 404))
    return planet

@planet_bp.route('/<planet_id>', methods = ['PUT'])
def modify_planet(planet_id):
    planet = validate_planet(planet_id)
    response_body = request.get_json()
    try:
        planet.name = response_body["name"]
        planet.description = response_body["description"]
        planet.population = response_body["population"]
    except KeyError:
        return make_response("You must input all of the following planet characteristics: name, description, population.")
    
    db.session.commit()

    return make_response(f'Planet with planet ID {planet.id} updated to {planet.name}')


@planet_bp.route('/<planet_id>', methods=['DELETE'])
def blow_planet_up(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f'Planet with ID {planet.id} targetted by death star',202)