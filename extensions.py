import json
import requests
from config import exchanges, commands


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        base_key = exchanges[base.lower()]
        sym_key = exchanges[sym.lower()]
        amount = float(amount)
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={amount}"
        headers = {"apikey": "mzajyAAI5aN3kY9i5rUS2DULx7joFlRp"}
        response = requests.get(url, headers=headers)
        result = json.loads(response.content)
        price = round(result['result'], 2)
        message = f'{amount} {base_key} = {price} {sym_key}'
        return message

    @staticmethod
    def stopping_conversion():
        text = f'Выполнение конвертации прервано! Список команд: \n'
        for i, k in enumerate(commands.items(), 1):
            text = '\n'.join((text, f'{i}. {k[0]} - {k[1]}'))
        return text

