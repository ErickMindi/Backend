from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/catalogodepto', methods=['POST'])
def create_catalogodepto():
    # Receiving Data
    NombreDepto = request.json['NombreDepto']
    Descripcion = request.json['Descripcion']
    Poblacion = request.json['Poblacion']

    if NombreDepto and Descripcion and Poblacion:
        id = mongo.db.catalogodepto.insert_one(
            {'NombreDepto': NombreDepto, 'Descripcion': Descripcion, 'Poblacion': Poblacion})
        response = jsonify({
            '_id': str(id),
            'NombreDepto': NombreDepto,
            'Descripcion': Descripcion,
            'Poblacion': Poblacion,
        })
        response.status_code = 201
        return response
    else:
        return not_found()
    
@app.route('/catalogodepto', methods=['GET'])
def get_catalogodeptos():
    catalogodeptos = mongo.db.catalogodepto.find()
    response = json_util.dumps(catalogodeptos)
    return Response(response, mimetype="application/json")


@app.route('/catalogodepto/<id>', methods=['GET'])
def get_catalogodepto(id):
    print(id)
    catalogodepto = mongo.db.catalogodepto.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(catalogodepto)
    return Response(response, mimetype="application/json")


@app.route('/catalogodepto/<id>', methods=['DELETE'])
def delete_catalogodepto(id):
    mongo.db.catalogodepto.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'catalogodepto' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/catalogodepto/<_id>', methods=['PUT'])
def update_catalogodepto(_id):
    NombreDepto = request.json['NombreDepto']
    Descripcion = request.json['Descripcion']
    Poblacion = request.json['Poblacion']
    if NombreDepto and Descripcion and Poblacion:
        mongo.db.catalogodepto.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'NombreDepto': NombreDepto, 'Descripcion': Descripcion, 'Poblacion': Poblacion}})
        response = jsonify({'message': 'catalogodepto' + _id + 'Updated Successfuly'})
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