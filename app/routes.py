from flask import Blueprint, jsonify

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