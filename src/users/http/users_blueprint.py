from flask import Blueprint, json, request, jsonify

from src.users.entities.user import User
from src.frameworks.http.cerberus import validate_schema
from src.utils.format_api_user import get_format, not_exist, get_all_format, create_format, delete_format, \
    conflict_unique_fields, update_format, get_average
from src.utils.constants import URL_PREFIX


ENTITY_NAME = "user"
ENTITY_NAME_PLURAL = "users"
URL = "/users"


def create_users_blueprint(manage_usecase):
    blueprint = Blueprint(f"{ENTITY_NAME_PLURAL}", __name__, url_prefix=URL_PREFIX)
    @blueprint.route(URL, methods=["GET"])
    def get_users():        
        users = manage_usecase.get_users()
        status_code = 200
        response = get_all_format(ENTITY_NAME_PLURAL, users)

        return response, status_code
    

    @blueprint.route(f"{URL}/<string:id>", methods=["GET"])
    def get_user(id):
        user = manage_usecase.get_user(id=id)
        if user:
            status_code = 200
            response = get_format(ENTITY_NAME, user)

        else:
            status_code = 409
            response = not_exist(ENTITY_NAME, id=id)

        return response, status_code

    @blueprint.route(URL, methods=["POST"])
    @validate_schema(User.validatable_fields, user_format_errors=True)
    def create_user():

        body = request.get_json(force=True)
        
        user, msg_error, type_error = manage_usecase.create_user(body)
        if user:
            status_code = 201
            response = create_format(ENTITY_NAME, user)
        else:
            if type_error == 409:
                status_code = type_error
                response = conflict_unique_fields(User.UNIQUE_FIELDS)
            else:
                status_code = 400
                response = {
                    "message": msg_error,
                    "code": "fail",
                }

        return response, status_code

    @blueprint.route(f"{URL}/<string:id>", methods=["PUT"])
    @validate_schema(User.validatable_fields, user_format_errors=True)
    def update_user(id):
        body = request.get_json(force=True)

        user, msg_error = manage_usecase.update_user(body,id=id)
        if user:
            status_code = 200
            response = update_format(ENTITY_NAME, user)
        else:
            status_code = 404
            response = {
                "message": msg_error,
                "code": "fail",
            } 

        return response, status_code


    @blueprint.route(f"{URL}/<string:id>", methods=["DELETE"])
    def delete_user(id):

        user = manage_usecase.delete_user(id=id)
        if user:
            status_code = 200
            response = delete_format(ENTITY_NAME, user)
        else:
            status_code = 404
            response = not_exist(ENTITY_NAME, id=id)

        return response, status_code
    
    @blueprint.route(f"{URL}/average", methods=["GET"])
    def get_user_average():

        user = manage_usecase.get_user_average()
        if user:
            status_code = 200
            response = get_average(ENTITY_NAME, user)
        else:
            status_code = 404
            response = not_exist(ENTITY_NAME, id=id)

        return response, status_code
    
    @blueprint.route(f"{URL}/status", methods=["GET"])
    def get_status():

        status = True
        if status:
            status_code = 200
            response = {
                "nameSystem": "api-users",
                "version": "1.0.0",
                "developer": "Darwin Acuña Vincenty",
                "email": "darwin182008@gmail.com",
                "message": "CRUD complete user"
            }

        return response, status_code
    
    return blueprint