from flask import Blueprint, jsonify, abort, make_response

planet_bp = Blueprint("planet_bp",__name__,url_prefix="/planets")

class Planet():
    def __init__(self, id, name, description, population):
        self.id = id
        self.name = name
        self.description = description
        self.population = population

planets = [Planet(1,"Mercury","It's solid",0),
        Planet(2,"Mars","It's red",1000000),
        Planet(3,"Earth","The blue marble",8000000000)]

@planet_bp.route('', methods=['GET'])
def get_all_planets():
    planet_list=[]
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
    for obj in planets:
        if obj.id==planet_id:
            return obj
    abort(make_response({"message":f"Planet with ID {planet_id} not in solar system"}, 404))