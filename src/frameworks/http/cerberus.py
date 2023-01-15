from functools import wraps

from cerberus import Validator
import cerberus

from flask import json, request, jsonify

# Decorador que valida la entrada JSON utilizando el Validator de la librería Cerberus.
# La función toma los datos obtenidos del JSON del request y los compara con el esquema
# de la clase. Si está OK continúa la ejecución y si falla retorna los errores del validador.


def validate_schema(schema, user_format_errors=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            json_data = request.get_json()
            validator = Validator()

            is_valid = validator.validate(json_data, schema)

            if is_valid:
                return f(*args, **kwargs)

            else:
                status_code = 422

                if user_format_errors:
                    response = generate_user_format_errors(validator)
                else:
                    data = validator.errors
                    response = {
                        "data": data,
                        "code": status_code,
                    }

                return response, status_code

        return wrapper

    return decorator


def generate_user_format_errors(validator):
    errors = []
    for field in validator.errors.keys():
        constraint = validator.document_error_tree.get(field).errors[0].constraint
        code = (f"{constraint}_" if constraint is not True else "") + "required"
        errors.append({
            "code": code,
            "message": validator.errors.get(field)[0],
            "field": field
        })
        
    response = {
        "errors": errors,
        "code": "fail",
        "message": "There was an error in input data."
    }
    
    
    return response

