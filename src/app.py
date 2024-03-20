"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User , People, Planet, UserFavorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/user', methods=['GET'])
def add_user():
     
    user= User.query.all()
    all_user = list(map(lambda x: x.serialize(), user))

    return jsonify(all_user), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    
    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    return jsonify(all_people), 200

@app.route('/planet', methods=['GET'])
def get_all_planet():
    
    planet = Planet.query.all()
    all_planet = list(map(lambda x: x.serialize(), planet))
    return jsonify(all_planet), 200


@app.route('/people/<int:id>', methods=['GET'])
def get_singleperson(id):

    # this is how you can use the Family datastructure by calling its methods
    person= People.query.get(id)
    test= person.serialize()

    return jsonify(test),200
   

@app.route('/user/<int:id>', methods=['GET'])
def get_singleUser(id):

    # this is how you can use the Family datastructure by calling its methods
    user= User.query.get(id)
    test= user.serialize()

    return jsonify(test),200
   
   
@app.route('/planet/<int:id>', methods=['GET'])
def get_singlePlanet(id):

    # this is how you can use the Family datastructure by calling its methods
    planet= Planet.query.get(id)
    test= planet.serialize()

    return jsonify(test),200
   


@app.route('/user/<id>/favorite', methods=['GET'])
def get_favofuser(id):

    fav= UserFavorite.query.filter_by(people_id =id)
    test2 = list(map(lambda x: x.serialize(), fav))

    return jsonify(test2),200
   



@app.route('/user', methods=['POST'])
def add_newuser():
        request_body=request.json
        
        test_user= User.query.filter_by(email=request_body['email']).first()
    
        if(test_user):
             return jsonify(f"User already exists"), 500
        
        else:
             newU=User(email=request_body['email'],password= request_body['password'] )
             db.session.add(newU)
             db.session.commit()
             return jsonify(f"Success"), 200
        


@app.route('/user/login', methods=['POST'])
def login_test():
        request_body=request.json
        
        test_user= User.query.filter_by(email=request_body[0]).first().id
        
        if(test_user):
            test_password= User.query.filter_by(email=request_body[0]).first().password
           # test_name= User.query.filter_by(email=request_body[0]).first().name
       
            if str(test_password)==request_body[1]:  
               #final=[test_user,str(test_name)]              
               return test_user
            else:
                 return jsonify(f"Incorrect email or password"), 400
                 
                       
        else:
              return jsonify(f"Incorrect email or password"), 400
       
        


@app.route('/favorite', methods=['POST'])
def add_favorite2():
      
        request_body=request.json
        test_user= User.query.filter_by(email=request_body['email'])
        test_people= People.query.filter_by(name=request_body['person'])
        test_planet= Planet.query.filter_by(name= request_body['planet'])

        test = list(map(lambda x: x.serialize(), test_user))
        test2 = list(map(lambda x: x.serialize(), test_people))
        test3 = list(map(lambda x: x.serialize(), test_planet))       
        
        if(test and test2 and test3):
            newfav = UserFavorite (user_id= test_user['id'], planets_id =test_planet['id'], people_id= test_people['id'])
            db.session.add(newfav)
            db.session.commit() 
            return jsonify(f"Success"), 200
        else:

            return  "either the email or the name or the planet doesnt exist", 200
     

@app.route('/favorite/<id>', methods=['DELETE'])
def delete_fav(id):
     
        p= UserFavorite.query.get(id)
        db.session.delete(p)
        db.session.commit()
        return jsonify(f"Success"), 200






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
