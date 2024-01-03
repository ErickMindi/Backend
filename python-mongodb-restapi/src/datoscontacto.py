from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/datoscontacto', methods=['POST'])
def create_datoscontacto():
    # Receiving Data
    TelFijo = request.json['TelFijo']
    TelCelular = request.json['TelCelular']
    IdWhatsApp = request.json['IdWhatsApp']
    IdTelegram = request.json['IdTelegram']
    ListaCorreos = request.json['ListaCorreos']

    if TelFijo and TelCelular and IdWhatsApp and IdTelegram and ListaCorreos:
        id = mongo.db.datoscontacto.insert_one(
            {'TelFijo': TelFijo, 'TelCelular': TelCelular, 'IdWahtsApp': IdWhatsApp, 'IdTelegram': IdTelegram, 'ListaCorreos': ListaCorreos})
        response = jsonify({
            '_id': str(id),
            'TelFijo': TelFijo,
            'TelCelular': TelCelular,
            'IdWhatsApp': IdWhatsApp,
            'IdTelegram': IdTelegram,
            'ListaCorreos': ListaCorreos
        })
        response.status_code = 201
        return response
    else:
        return not_found() 


@app.route('/datoscontacto', methods=['GET'])
def get_datoscontactos():
    datoscontactos = mongo.db.datoscontacto.find()
    response = json_util.dumps(datoscontactos)
    return Response(response, mimetype="application/json")


@app.route('/datoscontacto/<id>', methods=['GET'])
def get_datoscontacto(id):
    print(id)
    datoscontacto = mongo.db.datoscontacto.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(datoscontacto)
    return Response(response, mimetype="application/json")


@app.route('/datoscontacto/<id>', methods=['DELETE'])
def delete_datoscontacto(id):
    mongo.db.datoscontacto.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'datoscontacto' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/datoscontacto/<_id>', methods=['PUT'])
def update_datoscontacto(_id):
    TelFijo = request.json['TelFijo']
    TelCelular = request.json['TelCelular']
    IdWhatsApp = request.json['IdWhatsApp']
    IdTelegram = request.json['IdTelegram']
    ListaCorreos = request.json['ListaCorreos']
    if TelFijo and TelCelular and IdWhatsApp and IdTelegram and ListaCorreos:
        mongo.db.datoscontacto.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {'TelFijo': TelFijo, 'TelCelular': TelCelular, 'IdWahtsApp': IdWhatsApp, 'IdTelegram': IdTelegram, 'ListaCorreos': ListaCorreos}})
        response = jsonify({'message': 'datoscontacto' + _id + 'Updated Successfuly'})
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