from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/prestamo', methods=['POST'])
def create_prestamo():
    # Receiving Data
    MontoPrestamo = request.json['MontoPrestamo']
    TasaInteres = request.json['TasaInteres']
    FecSolicitud = request.json['FecSolicitud']
    FecAprobacion = request.json['FecAprobacion']
    FecVencimiento = request.json['FecVencimiento']
    PlazoMeses = request.json['PlazoMeses']
    MontoPendiente = request.json['MontoPendiente']
    PagosRealizados = request.json['PagosRealizados']
    CuotaMensual = request.json['CuotaMensual']
    MetodoPago = request.json['MetodoPago']

    if MontoPrestamo and TasaInteres and FecSolicitud and FecAprobacion and FecVencimiento and PlazoMeses and MontoPendiente and PagosRealizados and CuotaMensual and MetodoPago:
        id = mongo.db.prestamo.insert_one(
            {'MontoPrestamo': MontoPrestamo, 'TasaInteres': TasaInteres, 'FecSolicitud': FecSolicitud, 'FecAprobacion': FecAprobacion, 'FecVencimiento': FecVencimiento, 'PlazoMeses': PlazoMeses, 'MontoPendiente': MontoPendiente, 'PagosRealizados': PagosRealizados, 'CuotaMensual': CuotaMensual, 'MetodoPago': MetodoPago})
        response = jsonify({
            '_id': str(id),
            'MontoPrestamo': MontoPrestamo,
            'TasaInteres': TasaInteres,
            'FecSolicitud': FecSolicitud,
            'FecAprobacion': FecAprobacion,
            'FecVencimiento': FecVencimiento,
            'PlazoMeses': PlazoMeses,
            'MontoPendiente': MontoPendiente,
            'PagosRealizados': PagosRealizados,
            'CuotaMensual': CuotaMensual,
            'MetodoPago': MetodoPago
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/prestamo', methods=['GET'])
def get_prestamos():
    prestamos = mongo.db.prestamo.find()
    response = json_util.dumps(prestamos)
    return Response(response, mimetype="application/json")


@app.route('/prestamo/<id>', methods=['GET'])
def get_prestamo(id):
    print(id)
    prestamo = mongo.db.prestamo.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(prestamo)
    return Response(response, mimetype="application/json")


@app.route('/prestamo/<id>', methods=['DELETE'])
def delete_prestamo(id):
    mongo.db.prestamo.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Prestamo' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/prestamo/<_id>', methods=['PUT'])
def update_prestamo(_id):
    MontoPrestamo = request.json['MontoPrestamo']
    TasaInteres = request.json['TasaInteres']
    FecSolicitud = request.json['FecSolicitud']
    FecAprobacion = request.json['FecAprobacion']
    FecVencimiento = request.json['FecVencimiento']
    PlazoMeses = request.json['PlazoMeses']
    MontoPendiente = request.json['MontoPendiente']
    PagosRealizados = request.json['PagosRealizados']
    CuotaMensual = request.json['CuotaMensual']
    MetodoPago = request.json['MetodoPago']

    if MontoPrestamo and TasaInteres and FecSolicitud and FecAprobacion and FecVencimiento and PlazoMeses and MontoPendiente and PagosRealizados and CuotaMensual and MetodoPago:
        mongo.db.prestamo.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'MontoPrestamo': MontoPrestamo, 'TasaInteres': TasaInteres, 'FecSolicitud': FecSolicitud, 'FecAprobacion': FecAprobacion, 'FecVencimiento': FecVencimiento, 'PlazoMeses': PlazoMeses, 'MontoPendiente': MontoPendiente, 'PagosRealizados': PagosRealizados, 'CuotaMensual': CuotaMensual, 'MetodoPago': MetodoPago}})
        response = jsonify({'message': 'Prestamo' + _id + 'Updated Successfuly'})
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