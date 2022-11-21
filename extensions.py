import environment as env
import requests
import json


class APIException(Exception):
    """Custom exception"""
    pass


class Converter:

    @staticmethod
    def get_available_currencies():
        """Getting list of available currencies"""
        resp = requests.get(env.VALUES_URL, headers=env.HEADERS)
        if resp.status_code == 200:
            r = json.loads(resp.text)["currencies"]
            return r
        else:
            return APIException(f"Wrong status code from API {resp.status_code}")

    @staticmethod
    def get_price(base, quote, amount):
        """method for convertion request"""
        querystring = {f"format": "json", "from": {base}, "to": {quote},
                       "amount": {amount}}
        resp = requests.get(env.CONVERT_URL, headers=env.HEADERS, params=querystring)
        if resp.status_code == 200:
            r = json.loads(resp.text)
            return f"{r['amount']} {r['base_currency_name']} is equal to {r['rates'][quote]['rate_for_amount']} {r['rates'][quote]['currency_name']}"
        else:
            return APIException(f"Wrong status code from API {resp.status_code}")
