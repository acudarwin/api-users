
def not_exist(entity_name, **kwargs):
    errors = []
    for field in kwargs.keys():
        errors.append({
            "code": "not_exist",
            "message": f"Parameter '{kwargs.get(field)}' does not exist",
            "field": field
        })

    return fail_format(f"The {entity_name} specified does not exist.", errors)


def conflict_unique_fields(unique_fields):
    errors = []
    for field in unique_fields:
        errors.append({
            "code": "validation_error",
            "message": "This field must be unique",
            "field": field
        })

    return fail_format("There was an error in input data.", errors)


def get_format(entity_name, data):
    return success_format(data, f"The {entity_name} request was submitted successfully")

def get_average(entity_name, data):
    return average_format(data, f"The average {entity_name} request was submitted successfully")

def get_all_format(entity_name_plural, data):
    return success_format(data, f"The {entity_name_plural} request was submitted successfully.")


def create_format(entity_name, data):
    return success_format(data, f"The {entity_name} was created successfully")

def update_format(entity_name, data):
    return success_format(data, f"The {entity_name} was updated successfully")


def delete_format(entity_name, data):
    return success_format(data, f"The {entity_name} was deleted successfully")


def success_format(data, message, rest_data = {}):
    return {
        "data": data,
        "code": "success",
        "message": message,
        **rest_data #rest_data to append extra attributes (example: pagination data)
    }

def average_format(data, message, rest_data = {}):
    return {
        "average": data,
        "code": "success",
        "message": message,
        **rest_data 
    }


def fail_format(message, errors=[]):
    response = {
        "code": "fail",
        "message": message
    }
    response.update({"errors": errors} if errors else {})
    # Bugsnag logging
    
    return response
