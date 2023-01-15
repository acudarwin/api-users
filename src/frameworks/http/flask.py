import logging
import os

from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

MAX_FILES_MB_LENGTH = 10 #in MB

def create_flask_app(blueprints):
   
    # Función para crear una aplicación de Flask con todos sus blueprints (endpoints) asociados.

    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config['MAX_CONTENT_LENGTH'] = MAX_FILES_MB_LENGTH * 1024 * 1024
    
    app.register_error_handler(Exception, error_handler)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return {
            "data": "File too large",
            "code": "fail",
        }, 413

    
    return app


def error_handler(e):

    # Manejador de errores para excepciones genéricas. De esta forma se retorna
    # un JSON con el error en vez de retornar una página HTML en caso de error.

    # Igual se deben manejar los errores específicos en el blueprint; este handler
    # es sólo para las excepciones que no son manejadas manualmente.

    logging.exception(e)


    data = "Internal error during request."
    status_code = 500

    if isinstance(e, HTTPException):
        data = str(e)
        status_code = e.code

    response = {
        "data": data,
        "code": status_code,
    }

    return response, status_code


def get_user_header():

    # Retorna el valor de la cabecera "User-ID" desde el request,
    # o None si es que no está definida.

    return request.headers.get("User-ID")
