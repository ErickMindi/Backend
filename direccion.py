from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/direccion', methods=['POST'])
def create_direccion():
    # Receiving Data
    Calle = request.json['Calle']
    NumExterior = request.json['NumExterior']
    NumInterior = request.json['NumInterior']
    Manzana = request.json['Manzana']
    Lote = request.json['Lote']
    Municipio = request.json['Municipio']
    Ciudad = request.json['Ciudad']
    CodigoP = request.json['CodigoP']
    Pais = request.json['Pais']

    if Calle and NumExterior and NumInterior and Manzana and Lote and Municipio and Ciudad and CodigoP and Pais:
        id = mongo.db.direccion.insert_one(
            {'Calle': Calle, 'NumExterior': NumExterior, 'NumInterior': NumInterior, 'Manzana': Manzana, 'Lote': Lote, 'Municipio': Municipio, 'Ciudad': Ciudad, 'CodigoP': CodigoP, 'Pais': Pais})
        response = jsonify({
            '_id': str(id),
            'Calle': Calle,
            'NumExterior': NumExterior,
            'NumInterior': NumInterior,
            'Manzana': Manzana,
            'Lote': Lote,
            'Municipio': Municipio,
            'Ciudad': Ciudad,
            'CodigoP': CodigoP,
            'Pais': Pais
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/direccion', methods=['GET'])
def get_direccions():
    direccions = mongo.db.direccion.find()
    response = json_util.dumps(direccions)
    return Response(response, mimetype="application/json")


@app.route('/direccion/<id>', methods=['GET'])
def get_direccion(id):
    print(id)
    direccion = mongo.db.direccion.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(direccion)
    return Response(response, mimetype="application/json")


@app.route('/direccion/<id>', methods=['DELETE'])
def delete_direccion(id):
    mongo.db.direccion.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'direccion' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/direccion/<_id>', methods=['PUT'])
def update_direccion(_id):
    Calle = request.json['Calle']
    NumExterior = request.json['NumExterior']
    NumInterior = request.json['NumInterior']
    Manzana = request.json['Manzana']
    Lote = request.json['Lote']
    Municipio = request.json['Municipio']
    Ciudad = request.json['Ciudad']
    CodigoP = request.json['CodigoP']
    Pais = request.json['Pais']
    if Calle and NumExterior and NumInterior and Manzana and Lote and Municipio and Ciudad and CodigoP and Pais:
        mongo.db.direccion.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'Calle': Calle, 'NumExterior': NumExterior, 'NumInterior': NumInterior, 'Manzana': Manzana, 'Lote': Lote, 'Municipio': Municipio, 'Ciudad': Ciudad, 'CodigoP': CodigoP, 'Pais': Pais}})
        response = jsonify({'message': 'direccion' + _id + 'Updated Successfuly'})
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

    