from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost/controlempleados'

mongo = PyMongo(app)


@app.route('/rh', methods=['POST'])
def create_rh():
    # Receiving Data
    Puesto = request.json['Puesto']
    JefeInmediatoSup = request.json['JefeInmediatoSup']
    HorarioLaboral = request.json['HorarioLaboral']
    ExpedienteDigital = request.json['ExpedienteDigital']

    if Puesto and JefeInmediatoSup and HorarioLaboral and ExpedienteDigital:
        id = mongo.db.rh.insert_one(
            {'Puesto': Puesto, 'JefeInmediatoSup': JefeInmediatoSup, 'HorarioLaboral': HorarioLaboral, 'ExpedienteDigital': ExpedienteDigital})
        response = jsonify({
            '_id': str(id),
            'Puesto': Puesto,
            'JefeInmediatoSup': JefeInmediatoSup,
            'HorarioLaboral': HorarioLaboral,
            'ExpedienteDigital': ExpedienteDigital
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/rh', methods=['GET'])
def get_rhs():
    rhs = mongo.db.rh.find()
    response = json_util.dumps(rhs)
    return Response(response, mimetype="application/json")


@app.route('/rh/<id>', methods=['GET'])
def get_rh(id):
    print(id)
    rh = mongo.db.rh.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(rh)
    return Response(response, mimetype="application/json")


@app.route('/rh/<id>', methods=['DELETE'])
def delete_rh(id):
    mongo.db.rh.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Recurso Humano' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/rh/<_id>', methods=['PUT'])
def update_rh(_id):
    Puesto = request.json['Puesto']
    JefeInmediatoSup = request.json['JefeInmediatoSup']
    HorarioLaboral = request.json['HorarioLaboral']
    ExpedienteDigital = request.json['ExpedienteDigital']

    if Puesto and JefeInmediatoSup and HorarioLaboral and ExpedienteDigital:
        mongo.db.rh.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'Puesto': Puesto, 'JefeInmediatoSup': JefeInmediatoSup, 'HorarioLaboral': HorarioLaboral, 'ExpedienteDigital': ExpedienteDigital}})
        response = jsonify({'message': 'Recurso Humano ' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, port=3000)