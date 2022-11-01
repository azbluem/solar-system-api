from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    population = db.Column(db.BigInteger)
    
    def dictionfy(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "population": self.population
        }