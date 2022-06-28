import requests
import json
from config import exchanges

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.upper()]
        except KeyError:
            return ApiExceptions(f'Валюта {base} не найдена!')

        try:
            sym_key = exchanges[sym.upper()]
        except KeyError:
            return  ApiExceptions (f'Валюта {sym} не найдена!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ApiExceptions(f'Не удалось обработать количество {amount}!')

        if base_key == sym_key:
            raise ApiExceptions(f'Невозможно перевести одинаковые валюты {base}!')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={sym}&from={base}&amount={amount}"
        payload = {}
        headers = {
            "apikey": "DcXh02Osrr9bF4WxgeAE9JUPr7mDYToB"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        result = json.loads(response.content)
        new_price = result["result"]
        return new_price

class ApiExceptions(Exception):
    pass
