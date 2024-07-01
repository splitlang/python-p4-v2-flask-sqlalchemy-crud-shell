from flask import Flask, request, jsonify
from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

@app.route('/')
def index():
    return "Welcome to the Pet API!"

@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([pet.as_dict() for pet in pets])

@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = Pet.query.get_or_404(id)
    return jsonify(pet.as_dict())

@app.route('/pets', methods=['POST'])
def add_pet():
    data = request.get_json()
    new_pet = Pet(name=data['name'], species=data['species'])
    db.session.add(new_pet)
    db.session.commit()
    return jsonify(new_pet.as_dict()), 201

@app.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    data = request.get_json()
    pet = Pet.query.get_or_404(id)
    pet.name = data['name']
    pet.species = data['species']
    db.session.commit()
    return jsonify(pet.as_dict())

@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5555)
