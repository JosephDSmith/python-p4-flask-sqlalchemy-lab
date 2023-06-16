#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    zookeeper = Zookeeper.query.filter(Zookeeper.id == animal.zookeeper_id).first()
    enclosure = Enclosure.query.filter(Enclosure.id == animal.enclosure_id).first()

    response_body = (
    f'<ul>ID: {animal.id}</ul>\n'
    + f'<ul>Name: {animal.name}</ul>\n'
    + f'<ul>Species: {animal.species}</ul>\n'
    + f'<ul>Zookeeper: {zookeeper}</ul>\n'
    + f'<ul>Enclosure: {enclosure}</ul>\n'
)

    response = make_response(response_body, 200)

    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    animals = Animal.query.filter(Animal.zookeeper_id == zookeeper.id)

    response_body = (
    f'<ul>ID: {zookeeper.id}</ul>\n'
    + f'<ul>Name: {zookeeper.name}</ul>\n'
    + f'<ul>Birthday: {zookeeper.birthday}</ul>\n'
)
    for animal in animals:
        response_body += f'<ul>Animal: {animal}</ul>\n'


    response = make_response(response_body, 200)

    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):

    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    animals = Animal.query.filter(Animal.enclosure_id == enclosure.id)

    response_body = (
        f'<ul>ID: {enclosure.id}</ul>\n'
        + f'<ul>Environment: {enclosure.environment}</ul>\n'
        + f'<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>\n'
    )

    for animal in animals:
        response_body += f'<ul>Animal: {animal}</ul>\n'


    response = make_response(response_body, 200)

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
