from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/redsocial', methods=['POST'])
def create_redsocial():
    # Receiving Data
    UsuarioRed = request.json['UsuarioRed']
    Enlace = request.json['Enlace']

    if UsuarioRed and Enlace:
        id = mongo.db.redsocial.insert_one(
            {'UsuarioRed': UsuarioRed, 'Enlace': Enlace})
        response = jsonify({
            '_id': str(id),
            'UsuarioRed': UsuarioRed,
            'Enlace': Enlace
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/redsocial', methods=['GET'])
def get_redsocials():
    redsocials = mongo.db.redsocial.find()
    response = json_util.dumps(redsocials)
    return Response(response, mimetype="application/json")


@app.route('/redsocial/<id>', methods=['GET'])
def get_redsocial(id):
    print(id)
    redsocial = mongo.db.redsocial.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(redsocial)
    return Response(response, mimetype="application/json")


@app.route('/redsocial/<id>', methods=['DELETE'])
def delete_redsocial(id):
    mongo.db.redsocial.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Red Social' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/redsocial/<_id>', methods=['PUT'])
def update_redsocial(_id):
    UsuarioRed = request.json['UsuarioRed']
    Enlace = request.json['Enlace']

    if UsuarioRed and Enlace:
        mongo.db.redsocial.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'UsuarioRed': UsuarioRed, 'Enlace': Enlace}})
        response = jsonify({'message': 'Red Social' + _id + 'Updated Successfuly'})
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