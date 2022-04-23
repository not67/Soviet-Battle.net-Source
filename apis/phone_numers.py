import requests

from config import INI_CONFIG

token = INI_CONFIG['FIVESIM_API_KEY']

country = 'russia'
operator = 'any'
product = 'blizzard'

headers = {
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/json',
}


# test_number = {'id': 175764388, 'phone': '+79678866306', 'operator': 'beeline', 'product': 'blizzard', 'price': 2, 'status': 'PENDING',
#                'expires': '2021-10-19T09:30:25.642886475Z', 'sms': None, 'created_at': '2021-10-19T09:15:25.642886475Z', 'country': 'russia'}


def buy_number():
    response = requests.get('https://5sim.net/v1/user/buy/activation/' +
                            country + '/' + operator + '/' + product, headers=headers)

    return response.json()


# 175417574
def get_code(order_id):
    response = requests.get(
        'https://5sim.net/v1/user/check/' + str(order_id), headers=headers)

    data = response.json()
    for sms in data['sms']:
        if sms['code']:
            return sms['code']
