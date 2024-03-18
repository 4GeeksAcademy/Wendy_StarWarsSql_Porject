from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    




class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    surface = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(), unique=False, nullable=False)

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surface": self.surface,
            "climate": self.climate
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer(), unique=False, nullable=False)
    planet = db.Column(db.Integer(), db.ForeignKey("planet.id"))
    planet_link= db.relationship('Planet')
    
    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age
          
            # do not serialize the password, its a security breach
        }
    
class UserFavorite(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
     planets_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
     people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
     Planet= db.relationship('Planet')
     people= db.relationship('People')
     user= db.relationship('User')
    
     def __repr__(self):
        return '<UserFavorite %r>' % self.id

     def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,           
            "planets_id": self.planets_id,
            "people_id": self.people_id
             
            # do not serialize the password, its a security breach
        }
    
