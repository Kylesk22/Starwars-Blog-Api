from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Person(db.Model):
    __tablename__= 'Person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.String(80), unique=False, nullable=False)
    mass = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    skin_color = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    # favorites_id = db.Column(db.Integer, db.ForeignKey('Favorites.id'))



    def __repr__(self):
        return f'<User {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "gender": self.gender,
            # "favorites_id": self.favorites_id
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    __tablename__ = 'Planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    # favorites_id = db.Column(db.Integer, db.ForeignKey('Favorites.id'))

    
    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "mass": self.terrain,
            # "favorites_id": self.favorites_id
            
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    __tablename__ = 'Favorites'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey ('Person.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey ('Planet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    person = db.relationship('Person', lazy = True)
    planet = db.relationship('Planet', lazy = True)
    user = db.relationship('User', foreign_keys= [user_id])

    
    def __repr__(self):
       
        return f'<Favorites {self.person_id, self.planet_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
            
            # do not serialize the password, its a security breach
        }

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # fav_person = db.Column(db.String(120), unique=True, nullable=True)
    # fav_planet = db.Column(db.String(80), unique=True, nullable=True)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False)
    favorites = db.relationship('Favorites')

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # "fav_person": self.fav_person,
            # "fav_planet": self.fav_planet,
            # do not serialize the password, its a security breach
        }