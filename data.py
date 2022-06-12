import json


def load_from_json(file_name: json) -> list:
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


Users = load_from_json('users.json')
Orders = load_from_json('orders.json')
Offers = load_from_json('offers.json')

