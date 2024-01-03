from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
import logging
import json
from werkzeug.utils import secure_filename
import traceback
import base64
from bson.json_util import dumps
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash


def json_handler(obj):
    """Manejador para la serialización JSON que maneja ObjectId."""
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'application/json'

cors = CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost/controlempleados'

mongo = PyMongo(app)

logging.basicConfig(level=logging.DEBUG)


######################################################

#LOGIN
@app.route('/login', methods=['POST'])
def login():
    user = request.json.get('user')
    password = request.json.get('password')

    if not user or not password:
        return jsonify({"error": "Falta usuario o contraseña"}), 400

    usuario_db = mongo.db.usuario.find_one({'user': user})

    if usuario_db and check_password_hash(usuario_db['password'], password):
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

# REGISTRO USUARIO
@app.route('/usuario', methods=['POST'])
def create_usuario():
    user = request.json['user']
    password = request.json['password']

    if user and password:
        hashed_password = generate_password_hash(password)
        result = mongo.db.usuario.insert_one({'user': user, 'password': hashed_password})
        usuario_id = result.inserted_id
        response = jsonify({'_id': str(usuario_id), 'user': user})
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = mongo.db.usuario.find()
    response = dumps(usuarios)
    return response

@app.route('/usuario/<id>', methods=['GET'])
def get_usuario(id):
    usuario = mongo.db.usuario.find_one({'_id': ObjectId(id)})
    response = dumps(usuario)
    return response

@app.route('/usuario/<id>', methods=['PUT'])
def update_usuario(id):
    user = request.json['user']
    password = request.json['password']

    if user and password:
        usuario = {
            'user': user,
            'password': password
        }

        mongo.db.usuario.update_one({'_id': ObjectId(id)}, {'$set': usuario})
        response = jsonify({'message': 'Usuario ' + id + ' actualizado exitosamente'})
        response.status_code = 200
        return response
    else:
        return not_found()

@app.route('/usuario/<id>', methods=['DELETE'])
def delete_usuario(id):
    mongo.db.usuario.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Usuario ' + id + ' eliminado exitosamente'})
    response.status_code = 200
    return response

#EMPLEADOS

def generate_new_id():
    last_employee = mongo.db.empleados.find_one(sort=[("id", -1)])
    if last_employee:
        last_id = last_employee['id']
        return last_id + 1
    else:
        return 100001  # Empieza desde este número si no hay empleados

@app.route('/empleados', methods=['POST'])
def create_empleado():
    # Receiving Data
    Nombre = request.json['Nombre']
    ApelPaterno = request.json['ApelPaterno']
    ApelMaterno = request.json['ApelMaterno']
    FecNacimiento = request.json['FecNacimiento']
    Fotografia = None
    if 'Fotografia' in request.json:
        Fotografia = request.json['Fotografia']
    
    
    #Ruta = request.json['Ruta']

    if Nombre and ApelPaterno and ApelMaterno:
        emp = {'Nombre': Nombre, 'ApelPaterno': ApelPaterno, 'ApelMaterno': ApelMaterno, 
             'FecNacimiento':FecNacimiento,
        }
        if Fotografia:
            emp['Fotografia'] = Fotografia
        resultado = mongo.db.empleados.insert_one(emp
            )
        print("++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++")
        print("")
        response = jsonify({
            
            'Nombre': Nombre,
            'ApelPaterno': ApelPaterno,
            'ApelMaterno': ApelMaterno,
            'FecNacimiento': FecNacimiento,
            
            
        })
        response.status_code = 201
        return response
    else:
      return not_found()


@app.route('/empleados', methods=['GET'])
def get_empleados():
    empleados = mongo.db.empleados.find()
    
    response = json_util.dumps(empleados)
    response = json.loads(response)
    
     
    b = []
    for e in response:
        fn = ''
        if "Fotografia" in e:
            fn = e["Fotografia"]
        b.append({'_id': e["_id"]["$oid"],
            'Nombre': e["Nombre"],
            'ApelPaterno': e["ApelPaterno"],
            'ApelMaterno': e["ApelMaterno"],
            'FecNacimiento': e["FecNacimiento"],
            'Fotografia': fn,
        })
    b = json.dumps(b)
    return Response(b, mimetype="application/json")


@app.route('/empleados/<id>', methods=['GET'])
def get_empleado(id):
    print(id)
    empleado = mongo.db.empleados.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(empleado)
    return Response(response, mimetype="application/json")


@app.route('/empleados/<id>', methods=['DELETE'])
def delete_empleado(id):
    mongo.db.empleados.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'empleado' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/empleados/<id>', methods=['PUT'])
def update_empleado(id):
    Nombre = request.json['Nombre']
    ApelPaterno = request.json['ApelPaterno']
    ApelMaterno = request.json['ApelMaterno']
    FecNacimiento = request.json['FecNacimiento']
    
    
    Fotografia = None
    if 'Fotografia' in request.json:
        Fotografia = request.json['Fotografia']

  
    if Nombre and ApelPaterno and ApelMaterno and FecNacimiento and Fotografia:
        up = {'Nombre': Nombre, 'ApelPaterno': ApelPaterno, 'ApelMaterno': ApelMaterno, 'FecNacimiento': FecNacimiento}
        if Fotografia:
            up['Fotografia'] = Fotografia
        mongo.db.empleados.update_one(
            {'_id': ObjectId(id)}, {'$set': up})
        response = jsonify({'message': 'Empleado ' + id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()
#CATALOGO DEPARTAMENTOS

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

#COMPORTAMIENTO LABORAL

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

#DATOS CONTACTO

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

#DIRECCION

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

#EDUCACION


app.logger.setLevel(logging.DEBUG)

@app.route('/educacion', methods=['POST'])
def create_educacion():
    data = request.json
    empleado_id = data.get('empleado_id')

    app.logger.debug(f'Datos recibidos en la API: {data}')

    if empleado_id:
        educacion = []
        experiencia = []

        for edu in data.get('Educacion', []):
            educacion_item = {
                'Fecha': edu.get('Fecha'),
                'Titulo': edu.get('Titulo'),
                'Descripcion': edu.get('Descripcion')
            }
            educacion.append(educacion_item)

        for exp in data.get('Experiencia', []):
            experiencia_item = {
                'Fecha': exp.get('Fecha'),
                'Titulo': exp.get('Titulo'),
                'Descripcion': exp.get('Descripcion')
            }
            experiencia.append(experiencia_item)

        # Resto del código para insertar en la base de datos
        result = mongo.db.educacion.insert_one({
            'empleado_id': ObjectId(empleado_id),
            'Descripcion': data.get('Descripcion'),
            'Educacion': educacion,
            'Experiencia': experiencia,
            'Habilidades': data.get('Habilidades', {})
        })

        app.logger.debug(f'Resultado de la inserción en la base de datos: {result.inserted_id}')

        response = jsonify({
            '_id': str(result.inserted_id),
            'message': 'Datos de educación creados exitosamente'
        })
        response.status_code = 201
        return response
    else:
        app.logger.debug('Falta el ID del empleado')
        return jsonify({'message': 'Falta el ID del empleado'}), 400
    
    

@app.route('/educacion/empleado/<empleado_id>', methods=['GET'])
def get_educacion_by_empleado(empleado_id):
    try:
        empleado_object_id = ObjectId(empleado_id)
        educacion = mongo.db.educacion.find_one({'empleado_id': empleado_object_id})
        
        if educacion:
            # Asegúrate de que la estructura de la educación sea como se espera
            educacion_formato = {
                "_id": str(educacion["_id"]),
                "empleado_id": str(educacion["empleado_id"]),
                "Descripcion": educacion["Descripcion"],
                "Educacion": educacion["Educacion"],
                "Experiencia": educacion["Experiencia"],
                "Habilidades": educacion["Habilidades"]
            }

            # Devuelve la educación formateada como JSON
            response = jsonify(educacion_formato)
            app.logger.info(f"Datos de educación para el empleado {empleado_id} recuperados correctamente.")
            return response
        else:
            # Si no se encontró educación, devolver una respuesta 404
            app.logger.warning(f"No se encontraron datos de educación para el empleado {empleado_id}.")
            return jsonify({"error": "No se encontraron datos de educación para el empleado"}), 404
            
    except Exception as e:
        app.logger.error(f"Error al recuperar datos de educación para el empleado {empleado_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/educacion/<id>', methods=['DELETE'])
def delete_educacion(id):
    mongo.db.educacion.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'educaion' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/educacion/<empleado_id>', methods=['PUT'])
def update_educacion(empleado_id):
    data = request.get_json()
    if data:
        # Resto del código para procesar la actualización en la base de datos
        result = mongo.db.educacion.update_one(
            {'empleado_id': ObjectId(empleado_id['$oid']) if '$oid' in empleado_id else ObjectId(empleado_id)},
            {'$set': {
                'Descripcion': data.get('Descripcion'),
                'Educacion': data.get('Educacion'),
                'Experiencia': data.get('Experiencia'),
                'Habilidades': data.get('Habilidades')
            }}
        )

        if result.modified_count > 0:
            response = jsonify({'message': 'Educacion ' + empleado_id + ' updated successfully'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Educacion ' + empleado_id + ' not found'})
            response.status_code = 404
            return response
    else:
        return jsonify({'error': 'Invalid JSON data'}), 400


    

#EXPEDIENTE CLINICO


@app.route('/expedienteclinico', methods=['POST'])
def create_expediente_clinico():
    try:
        data = request.get_json()

        empleado_id = data.get('empleado_id')
        tipo_sangre = data.get('tipoSangre')
        padecimientos = data.get('Padecimientos')
        num_ss = data.get('NumeroSeguroSocial')
        seguro_gastos_medicos = data.get('Segurodegastosmedicos')
        pdf_seguro_gastos_medicos = data.get('PDFSegurodegastosmedicos')

        expediente_clinico_data = {
            'empleado_id': ObjectId(empleado_id),
            'TipoSangre': tipo_sangre,
            'Padecimientos': padecimientos,
            'NumSS': num_ss,
            'SeguroGastosMedicosMayores': seguro_gastos_medicos,
            'PDFSeguroGastosMedicosMayores': pdf_seguro_gastos_medicos
        }

        result = mongo.db.expedienteclinico.insert_one(expediente_clinico_data)

        return jsonify({'inserted_id': str(result.inserted_id)}), 200

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal server error'}), 500




@app.route('/expedienteclinico/empleado/<empleado_id>', methods=['GET'])
def get_expedienteclinicos_by_empleado(empleado_id):
    try:
        expedienteclinicoss = mongo.db.expedienteclinico.find({'empleado_id': ObjectId(empleado_id)})

        response = json_util.dumps(expedienteclinicoss)
        return Response(response, mimetype="application/json")

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal server error'}), 500

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


@app.route('/expedienteclinico/empleado/<empleado_id>', methods=['PUT'])
def update_expedienteclinico_empleado(empleado_id):
    try:
        empleado_id_obj = ObjectId(empleado_id)
        data = request.get_json()
        expediente_clinico_nuevo = data  # Ahora asumimos que recibes el objeto directamente

        existing_data = mongo.db.expedienteclinico.find_one({'empleado_id': empleado_id_obj})

        if existing_data:
            mongo.db.expedienteclinico.update_one(
                {'empleado_id': empleado_id_obj},
                {
                    '$set': {
                        'tipoSangre': expediente_clinico_nuevo.get('tipoSangre'),
                        'Padecimientos': expediente_clinico_nuevo.get('Padecimientos'),
                        'NumeroSeguroSocial': expediente_clinico_nuevo.get('NumeroSeguroSocial'),
                        'Segurodegastosmedicos': expediente_clinico_nuevo.get('Segurodegastosmedicos'),
                        'PDFSegurodegastosmedicos': expediente_clinico_nuevo.get('PDFSegurodegastosmedicos'),
                    }
                }
            )

            response = jsonify({
                'empleado_id': str(empleado_id_obj),
                'message': 'Datos de expediente clínico actualizados exitosamente'
            })
            response.status_code = 200
            return response
        else:
            result = mongo.db.expedienteclinico.insert_one({
                'empleado_id': empleado_id_obj,
                'tipoSangre': expediente_clinico_nuevo.get('tipoSangre'),
                'Padecimientos': expediente_clinico_nuevo.get('Padecimientos'),
                'NumeroSeguroSocial': expediente_clinico_nuevo.get('NumeroSeguroSocial'),
                'Segurodegastosmedicos': expediente_clinico_nuevo.get('Segurodegastosmedicos'),
                'PDFSegurodegastosmedicos': expediente_clinico_nuevo.get('PDFSegurodegastosmedicos'),
            })
            print(f'Resultado de la inserción en la base de datos: {result.inserted_id}')

            response = jsonify({
                'empleado_id': str(empleado_id_obj),
                'message': 'Datos de expediente clínico creados exitosamente'
            })
            response.status_code = 201
            return response

    except Exception as e:
        print("Error:", e)
        return jsonify({'message': 'Error al actualizar expediente clínico del empleado'}), 500
    
#PERSONAS CONTACTO

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

#PRESTAMO

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

#RED SOCIAL

@app.route('/redsocial', methods=['POST'])
def create_or_update_redsocial():
    try:
        data = request.get_json()
        empleado_id = data.get('empleado_id')
        redes_sociales = data.get('RedesSociales', [])

        if empleado_id:
            # Verifica si ya hay datos para este empleado en la colección
            existing_data = mongo.db.redsocial.find_one({'empleado_id': ObjectId(empleado_id)})

            if existing_data:
                # Actualiza el registro existente
                mongo.db.redsocial.update_one(
                    {'empleado_id': ObjectId(empleado_id)},
                    {
                        '$set': {
                            'RedesSociales': redes_sociales
                        }
                    }
                )
            else:
                # Inserta un nuevo registro si no hay datos existentes
                result = mongo.db.redsocial.insert_one({
                    'empleado_id': ObjectId(empleado_id),
                    'RedesSociales': redes_sociales
                })
                print(f'Resultado de la inserción en la base de datos: {result.inserted_id}')

            response = jsonify({
                'empleado_id': empleado_id,
                'message': 'Datos de redes sociales creados o actualizados exitosamente'
            })
            response.status_code = 201
            return response
        else:
            return jsonify({'error': 'Datos insuficientes para crear o actualizar redes sociales'}), 400

    except Exception as e:
        # Imprimir cualquier excepción que pueda ocurrir
        print("Error:", e)
        return jsonify({'message': 'Error al procesar la solicitud'}), 500



@app.route('/redsocial/empleado/<empleado_id>', methods=['GET'])
def get_redessociales_empleado(empleado_id):
    try:
        empleado_id_obj = ObjectId(empleado_id)
        print("Empleado ID (solicitud):", empleado_id)
        print("Empleado ID (convertido a ObjectId):", empleado_id_obj)

        # Cambié 'redessociales' a 'redsocial' en la siguiente línea
        redes_sociales = mongo.db.redsocial.find({'empleado_id': empleado_id_obj})
        result = list(redes_sociales)


        formatted_result = []
        for red_social in result:
            redes_sociales_list = red_social.get('RedesSociales', [])
            redes_sociales_item = {
                '_id': str(red_social['_id']),
                "empleado_id": str(red_social['empleado_id']),
                'RedesSociales': [
                    {
                        'redSocialSeleccionada': red.get('redSocialSeleccionada', ''),
                        'URLRedSocial': red.get('URLRedSocial', ''),
                        'NombreRedSocial': red.get('NombreRedSocial', '')
                    } for red in redes_sociales_list
                ]
            }
            formatted_result.append(redes_sociales_item)


        # Devolver una lista vacía si no hay resultados
        return jsonify(formatted_result if formatted_result else [])
    except Exception as e:
        # Imprimir cualquier excepción que pueda ocurrir
        print("Error:", e)
        return jsonify({'message': 'Error en la consulta de redes sociales'}), 500


    

@app.route('/redsocial/<id>', methods=['DELETE'])
def delete_redsocial(id):
    mongo.db.redsocial.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Red Social' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/redsocial/empleado/<empleado_id>', methods=['PUT'])
def update_redessociales_empleado(empleado_id):
    try:
        empleado_id_obj = ObjectId(empleado_id)
        data = request.get_json()
        redes_sociales_nuevas = data.get('RedesSociales', [])

        existing_data = mongo.db.redsocial.find_one({'empleado_id': empleado_id_obj})

        if existing_data:
      
            mongo.db.redsocial.update_one(
                {'empleado_id': empleado_id_obj},
                {
                    '$set': {
                        'RedesSociales': redes_sociales_nuevas
                    }
                }
            )

            response = jsonify({
                'empleado_id': str(empleado_id_obj),
                'message': 'Datos de redes sociales actualizados exitosamente'
            })
            response.status_code = 200
            return response
        else:
           
            result = mongo.db.redsocial.insert_one({
                'empleado_id': empleado_id_obj,
                'RedesSociales': redes_sociales_nuevas
            })
            print(f'Resultado de la inserción en la base de datos: {result.inserted_id}')

            response = jsonify({
                'empleado_id': str(empleado_id_obj),
                'message': 'Datos de redes sociales creados exitosamente'
            })
            response.status_code = 201
            return response

    except Exception as e:
    
        print("Error:", e)
        return jsonify({'message': 'Error al actualizar redes sociales del empleado'}), 500
    

#RECURSOS HUMANOS

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

########################################################
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

    