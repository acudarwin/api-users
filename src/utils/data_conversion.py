import json


def dict_to_bytes(dict):

    return json.dumps(dict).encode("utf-8")


def bytes_to_dict(bytes):

    return json.loads(bytes.decode("utf-8"))


def fields_to_dict(fields):

    # Transforma la lista de campos que incluyen sus tipos de valor,
    # dejándolo como un simple diccionario en Python.

    json_dict = {}

    for key, value in fields.items():
        json_dict[key] = get_field_value(value)

    return json_dict


def get_field_value(field):

    # Transforma un campo específico al tipo de dato correcto.
    # Se aplica recursión en el caso de que sea una lista o diccionario.

    field_type = list(field)[0]
    field_content = field[field_type]

    real_value = None

    if field_type in [
        "timestampValue",
        "stringValue",
        "bytesValue",
        "referenceValue",
        "booleanValue",
        "nullValue",
        "geoPointValue",
    ]:
        real_value = field_content

    elif field_type == "integerValue":
        real_value = int(field_content)

    elif field_type == "doubleValue":
        real_value = float(field_content)

    elif field_type == "arrayValue":

        real_value = []

        for sub_value in field_content["values"]:
            real_value.append(get_field_value(sub_value))

    elif field_type == "mapValue":

        real_value = {}

        for sub_key, sub_value in field_content["fields"].items():
            real_value[sub_key] = get_field_value(sub_value)

    return real_value
