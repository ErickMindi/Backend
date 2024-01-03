from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://database/controlempleados'

mongo = PyMongo(app)


@app.route('/educacion', methods=['POST'])
def create_educacion():
    # Receiving Data
    MaxGradoEstudios = request.json['MaxGradoEstudios']
    Experiencia = request.json['Experiencia']
    Habilidades = request.json['Habilidades']
    ListaCursos = request.json['ListaCursos']

    if MaxGradoEstudios and Experiencia and Habilidades and ListaCursos:
        id = mongo.db.educacion.insert_one(
            {'MaxGradoEstudios': MaxGradoEstudios, 'Experiencia': Experiencia, 'Habilidades': Habilidades, 'ListaCursos': ListaCursos})
        response = jsonify({
            '_id': str(id),
            'MaxGardoEstudios': MaxGradoEstudios,
            'Experiencia': Experiencia,
            'Habilidades': Habilidades,
            'ListaCursos': ListaCursos
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/educacion', methods=['GET'])
def get_educacions():
    educacions = mongo.db.educacion.find()
    response = json_util.dumps(educacions)
    return Response(response, mimetype="application/json")


@app.route('/educacion/<id>', methods=['GET'])
def get_educacion(id):
    print(id)
    educacion = mongo.db.educacion.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(educacion)
    return Response(response, mimetype="application/json")


@app.route('/educacion/<id>', methods=['DELETE'])
def delete_educacion(id):
    mongo.db.educacion.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'educaion' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/educacion/<_id>', methods=['PUT'])
def update_educacion(_id):
    MaxGradoEstudios = request.json['MaxGradoEstudios']
    Experiencia = request.json['Experiencia']
    Habilidades = request.json['Habilidades']
    ListaCursos = request.json['ListaCursos']
    if MaxGradoEstudios and Experiencia and Habilidades and ListaCursos:
        mongo.db.educacion.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'MaxGradoEstudios': MaxGradoEstudios, 'Experiencia': Experiencia, 'Habilidades': Habilidades, 'ListaCursos': ListaCursos}})
        response = jsonify({'message': 'educacion' + _id + 'Updated Successfuly'})
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