from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active
        }
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id')) 
    

    def serialize(self):
        name = ''
        user = User.query.get(self.user_id).serialize()
        if self.planet_id:
            name = Planet.query.get(self.planet_id).name
        return {
            'user_id': self.user_id,
            'planet_id': self.planet_id,
            'people_id': self.people_id,
            'planet_name': name,
            'user':user
        }
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def __repr__(self):
        return f'<Planet {self.name}>'
    
    def __init__(self, name, climate, terrain, population):
        self.name = name
        self.climate = climate
        self.terrain = terrain
        self.population = population

    def serialize(self):
        return {
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    homeworld = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('Favorite', backref='people', lazy=True)

    def __repr__(self):
        return f'<People {self.name}>'

    def __init__(self, name, height, mass, gender, homeworld):
        self.name = name
        self.height = height
        self.mass = mass
        self.gender = gender
        self.homeworld = homeworld

    def serialize(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,        
            "homeworld": self.homeworld
        }
