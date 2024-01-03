from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/comportamientolaboral', methods=['POST'])
def create_comportamientolaboral():
    # Receiving Data
    Fecha = request.json['Fecha']
    Descripcion = request.json['Descripcion']
    Calificacion = request.json['Calificacion']

    if Fecha and Descripcion and Calificacion:
        id = mongo.db.comportamientolaboral.insert_one(
            {'Fecha': Fecha, 'Descripcion': Descripcion, 'Calificacion': Calificacion})
        response = jsonify({
            '_id': str(id),
            'Fecha': Fecha,
            'Descripcion': Descripcion,
            'Calificacion': Calificacion
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/comportamientolaboral', methods=['GET'])
def get_comportamientolaborals():
    comportamientolaborals = mongo.db.comportamientolaboral.find()
    response = json_util.dumps(comportamientolaborals)
    return Response(response, mimetype="application/json")


@app.route('/comportamientolaboral/<id>', methods=['GET'])
def get_comportamientolaboral(id):
    print(id)
    comportamientolaboral = mongo.db.comportamientolaboral.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(comportamientolaboral)
    return Response(response, mimetype="application/json")


@app.route('/comportamientolaboral/<id>', methods=['DELETE'])
def delete_comportamientolaboral(id):
    mongo.db.comportamientolaboral.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'comportamientolaboral' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/comportamientolaboral/<_id>', methods=['PUT'])
def update_comportamientolaboral(_id):
    Fecha = request.json['Fecha']
    Descripcion = request.json['Descripcion']
    Calificacion = request.json['Calificacion']
    if Fecha and Descripcion and Calificacion:
        mongo.db.comportamientolaboral.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'Fecha': Fecha, 'Descripcion': Descripcion, 'Calificacion': Calificacion}})
        response = jsonify({'message': 'comportamientolaboral' + _id + 'Updated Successfuly'})
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