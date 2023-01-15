import logging

import requests
from datetime import datetime, timezone, time

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
HOURS_FORMAT = "%H:%M:%S"


class AkihabaraConnector:
    def __init__(self, endpoint, environment):
        self.endpoint = endpoint
        self.environment = environment

    def get_headers(self, carrier_code):
        headers = {
            "Content-Type": "application/json",
            "x-carrier": carrier_code,
            "Accept": "application/json",
            "x-env": "false",
        }
        if self.environment != "production":
            headers.update({"x-carrier": carrier_code})
            headers.update({"x-laravel-debug": "true"})

        return headers

    def __create_akihabara_payload(self, shipper_id, data):
        code = data.get("shipper_code")
        type_carrier = data.get("type")
        data = data.get("data", {})
        customization = data.get("customization", {})
        payload = {
            "code": code,
            "shipper_id": shipper_id,
            "credentials": {},
            "data": data,
            "customization": customization,
        }
        if type_carrier.startswith("sel"):
            parent_id = data.get("parent_id")
            payload["parent_id"] = parent_id
        elif type_carrier.startswith("pas"):
            payload["credentials"] = data.get("credentials")

        return payload

    def __update_akihabara_payload(self, carrier_code, carrier, new_data):
        code = carrier_code
        type_carrier = new_data.get("type")
        data = new_data.get("data", {})
        customization = new_data.get("customization", {})
        payload = {
            "code": code,
            "credentials": {},
            "data": data,
            "customization": customization,
        }
        if type_carrier.startswith("sel"):
            payload["parent_id"] = new_data.get("parent_id")
        elif type_carrier.startswith("pas"):
            payload["credentials"] = new_data.get("credentials")

        return payload

    def create_akihabara_account(self, shipper_id, data):
        headers = self.get_headers(data["carrier_code"])
        logging.info(f"creando cuenta en akihabara, data: {data}")
        payload = self.__create_akihabara_payload(shipper_id, data)
        url = f"{self.endpoint}/api/shippers/{shipper_id}/accounts"
        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
        )
        print(url)
        print(headers)
        return response

    def update_akihabara_account(self, carrier_code, carrier, data):
        print("carrier_code")
        print(carrier_code)
        headers = self.get_headers(carrier_code)
        logging.info(f"actualizando cuenta en akihabara, data: {data}")
        payload = self.__update_akihabara_payload(carrier_code, carrier.shipper_id, data)
        url = f"{self.endpoint}/api/shippers/{carrier.shipper_id}/accounts/{carrier.account_id}"
        response = requests.put(
            url=url,
            json=payload,
            headers=headers,
        )
        print(url)
        print(headers)
        print(payload)
        return response


def format_date(datetime):
    # Retorna una representación en String de una fecha/hora dada.
    if datetime:
        return datetime.strftime(DATE_FORMAT)
    else:
        return None
    
def hours_date(var_time):
    # Retorna una representación en String de una hora dada.
    formato = str(var_time).split(":")
    horas=int(formato[0])
    minutos=int(formato[1])
    formato_final = time(horas, minutos)
    return formato_final.isoformat()

def get_current_datetime():

    # Retorna la fecha actual en UTC-0
    
    return datetime.now(timezone.utc)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions
