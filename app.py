from flask import Flask, request
from dbhelpers import run_statement
import json

app = Flask(__name__)

@app.get('/hello')
def get_hello():
    return "Hello World"

@app.get('/api/animals')
def get_animals():
    result = run_statement("CALL get_animals()")
    if (type(result) == list):
        result_json = json.dumps(result, default=str)
        return result_json
    else:
        return "Sorry, something went wrong"

@app.post('/api/make_animals')
def make_animals():
    animals_name = request.json.get('animalsName')
    animals_class = request.json.get('animalsClass')
    animals_diet = request.json.get('animalsDiet')
    if animals_name == None:
        return "You must specify an animal name"
    if animals_class == None:
        return "You must specify the class of animal"
    if animals_diet == None:
        return "You must specify the animal diet"
    result = run_statement("CALL make_animals(?,?,?)", [animals_name, animals_class, animals_diet])
    if result == None:
        return "Success"
    else:
        return "Something went terribly wrong"

@app.patch('/api/edit_animals')
def edit_animals():
    animals_name = request.json.get('animalsName')
    animals_class = request.json.get('animalsClass')
    if animals_name == None:
        return "You must specify an animal name to edit"
    if animals_class == None:
        return "You must specify the class of animal to edit"
    result = run_statement("CALL edit_animals(?,?)", [animals_name, animals_class])
    if result == None:
        return "Success"
    else:
        return "Unable to update animal name"
    

@app.delete('/api/delete_animals')
def delete_animals():
    animals_name = request.json.get('animalsName')
    if animals_name == None:
        return "You must specify an animal to delete"
    result = run_statement("CALL delete_animals(?)", [animals_name])
    if result == None:
        return "Success"
    else:
        return "Unable to delete animal"

app.run(debug = True)