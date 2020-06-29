from flask import Flask , jsonify, request
from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields 
from marshmallow.exceptions import ValidationError
# from marshmallow import validate
from marshmallow.validate import Range

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "postgres://postgres:postgres@localhost:5432/postgres"
# Db = "postgres://YourUserNme:YourPassword@YourHost:5432/YourDatabase";
db=SQLAlchemy()
ma=Marshmallow()

db.init_app(app)
ma.init_app(app)


Column , String , Integer , Model= db.Column , db.String , db.Integer, db.Model 



class Animal(db.Model):
    
    __tablename__="animals"

    id=db.Column(db.Integer(),primary_key=True)
    name =db.Column(db.String())
    # owner_id=db.Column(db.Integer(),db.ForeignKey('owner.id'))
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,**kwargs):
        for key , value in kwargs.items():
            setattr(self,key ,value)

        self.save()

# class Owner(db.Model):
#     __tablename__="owner"
#     id=db.Column(db.Integer(),primary_key=True)
#     name=db.Column(db.String(50))
#     animal=db.relationship('Animal',backref='owner', uselist=False)


class AnimalSerializer(ma.SQLAlchemyAutoSchema):

    name =fields.String(required=True)


    class Meta:
        model=Animal

        load_instance = True

with app.app_context():
    db.create_all()  

@app.route("/", methods=["GET"])
def func():

    return jsonify(message="salam baki"), HTTPStatus.OK


@app.route("/animals" , methods=["GET"])
def get_animals():

    animals=Animal.query.all()
    return AnimalSerializer().jsonify(animals,many=True),HTTPStatus.OK


@app.route("/animals/<int:id>", methods=["GET"])
def get_animal(id):

    animal=Animal.query.filter_by(id=id).first()
    
    return AnimalSerializer().jsonify(animal), HTTPStatus.OK


@app.route("/animals",methods=["POST"])
def create_animal():

    try:
        data=request.get_json()
        serializer=AnimalSerializer()
        animal=serializer.load(data)

        animal.save()

        return AnimalSerializer().jsonify(animal)
    except ValidationError as err:
        print(err.messages)

        return jsonify({"result":err.messages}), HTTPStatus.BAD_REQUEST

    


@app.route("/animals/<int:id>", methods=["PUT"])
def update_animal(id):

    data=request.get_json()
    print(data)
    animal=Animal.query.filter_by(id=id).first()
    serializer=AnimalSerializer()

    animals=serializer.dump(data)
    
    print(animals)

    animals_up=animal.update(**animals)

    return AnimalSerializer().jsonify(animal)
    

@app.route("/animals/<int:id>", methods=["DELETE"])
def delete_animal(id):
    animal=Animal.query.get(id)

    if animal:
        animal.delete()

        return jsonify({"result":True}), HTTPStatus.OK
    
    return jsonify({"result":False,
    "message":"no animals found"}), HTTPStatus.BAD_REQUEST




