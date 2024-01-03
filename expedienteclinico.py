from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/expedienteclinico', methods=['POST'])
def create_expedienteclinico():
    # Receiving Data
    TipoSangre = request.json['TipoSangre']
    Padecimientos = request.json['Padecimientos']
    NumSS = request.json['NumSS']
    SeguroGastosMedicosMayores = request.json['SeguroGastosMedicosMayores']
    Estudios = request.json['Estudios']

    if TipoSangre and Padecimientos and NumSS and SeguroGastosMedicosMayores and Estudios:
        id = mongo.db.expedienteclinico.insert_one(
            {'TipoSangre': TipoSangre, 'Padecimientos': Padecimientos, 'NumSS': NumSS, 'SeguroGastosMedicosMayores': SeguroGastosMedicosMayores, 'Estudios': Estudios})
        response = jsonify({
            '_id': str(id),
            'TipoSangre': TipoSangre,
            'Padecimientos': Padecimientos,
            'NumSS': NumSS,
            'SeguroGastosMedicosMayores': SeguroGastosMedicosMayores,
            'Estudios': Estudios
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/expedienteclinico', methods=['GET'])
def get_expedienteclinicos():
    expedienteclinicoss = mongo.db.expedienteclinico.find()
    response = json_util.dumps(expedienteclinicoss)
    return Response(response, mimetype="application/json")


@app.route('/expedienteclinico/<id>', methods=['GET'])
def get_expedienteclinico(id):
    print(id)
    expedienteclinico = mongo.db.expedienteclinico.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(expedienteclinico)
    return Response(response, mimetype="application/json")


@app.route('/expedienteclinico/<id>', methods=['DELETE'])
def delete_expedienteclinico(id):
    mongo.db.expedienteclinico.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Expediente Clinico' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/expedienteclinico/<_id>', methods=['PUT'])
def update_expedienteclinico(_id):
    TipoSangre = request.json['TipoSangre']
    Padecimientos = request.json['Padecimientos']
    NumSS = request.json['NumSS']
    SeguroGastosMedicosMayores = request.json['SeguroGastosMedicosMayores']
    Estudios = request.json['Estudios']
    if TipoSangre and Padecimientos and NumSS and SeguroGastosMedicosMayores and Estudios:
        mongo.db.expedienteclinico.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'TipoSangre': TipoSangre, 'Padecimientos': Padecimientos, 'NumSS': NumSS, 'SeguroGastosMedicosMayores': SeguroGastosMedicosMayores, 'Estudios': Estudios}})
        response = jsonify({'message': 'Expediente Clinico' + _id + 'Updated Successfuly'})
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