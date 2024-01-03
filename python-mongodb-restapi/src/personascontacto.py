from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/personascontacto', methods=['POST'])
def create_personascontacto():
    # Receiving Data
    ParentescoEmpleado = request.json['ParentescoEmpleado']
    Empleado = request.json['Empleado']
    DatosContacto = request.json['DatosContacto']

    if ParentescoEmpleado and Empleado and DatosContacto:
        id = mongo.db.personascontacto.insert_one(
            {'ParentescoEmpleado': ParentescoEmpleado, 'Empleado': Empleado, 'DatosContacto': DatosContacto})
        response = jsonify({
            '_id': str(id),
            'ParentescoEmpleado': ParentescoEmpleado,
            'Empleado': Empleado,
            'DatosContacto': DatosContacto
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/personascontacto', methods=['GET'])
def get_personascontactos():
    personascontactos = mongo.db.personascontacto.find()
    response = json_util.dumps(personascontactos)
    return Response(response, mimetype="application/json")


@app.route('/personascontacto/<id>', methods=['GET'])
def get_personascontacto(id):
    print(id)
    personascontacto = mongo.db.personascontacto.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(personascontacto)
    return Response(response, mimetype="application/json")


@app.route('/personascontacto/<id>', methods=['DELETE'])
def delete_personascontacto(id):
    mongo.db.personascontacto.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Persona Contacto' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/personascontacto/<_id>', methods=['PUT'])
def update_personascontacto(_id):
    ParentescoEmpleado = request.json['ParentescoEmpleado']
    Empleado = request.json['Empleado']
    DatosContacto = request.json['DatosContacto']

    if ParentescoEmpleado and Empleado and DatosContacto:
        mongo.db.personascontacto.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'ParentescoEmpleado': ParentescoEmpleado, 'Empleado': Empleado, 'DatosContacto': DatosContacto}})
        response = jsonify({'message': 'Persona Contacto' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, port=3000)