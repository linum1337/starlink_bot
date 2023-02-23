

import requests
ip_out = '85.26.197.246:8082'
ip_inner = '85.26.197.246:8082'
def tg_id(abonent_id, tg):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = 'method1=objects.create&arg1={"abonent_id":"' + str(abonent_id) + '","attribute_id":"1012","attribute_value":"'+ str(tg) + '"}'

    response = requests.post('http://' + ip_inner + ':8082:8082/rest_api/v2/AttributeValues/', headers=headers, data=data)
    print(response)


def abon_id(login):
    import requests

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = 'method1=objects.filter&arg1={"login":"' + login + '"}'

    response = requests.post('http://' + ip_inner + '/rest_api/v2/Users/', headers=headers, data=data).json()
    return response['result'][0]['fields']['abonent_id']
def abon_balance(abon_id):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = 'method1=objects.get&arg1={"account_id_abonents":"' + str(abon_id) + '"}&fields=["balance"]'

    response = requests.post('http://' + ip_inner + '/rest_api/v2/AdminAccounts/', headers=headers, data=data).json()
    return response['result']['fields']['balance']
def abon_tarif(abon_id):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = 'method1=objects.get&arg1={"id":"' + str(abon_id) + '"}&fields=["tarif_id"]'

    response = requests.post('http://' + ip_inner + '/rest_api/v2/Abonents/', headers=headers, data=data).json()
    tarif_id = str(response['result']['fields']['tarif_id'])
    data_for_tarif = 'method1=objects.get&arg1={"id":"' + str(tarif_id) + '"}&fields=["name"]'
    response_for_tarif = requests.post('http://' + ip_inner + '/rest_api/v2/Tarif/', headers=headers, data=data_for_tarif).json()
    return response_for_tarif['result']['fields']['name']

def abon_usluga(abon_id):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = 'method1=objects.filter&arg1={"abonent_id":' + str(abon_id) + '}&fields=["usluga__name","usluga__comments","comment"]'

    response = requests.post('http://' + ip_inner + '/rest_api/v2/UsersUsluga/', headers=headers, data=data).json()
    uslugi = []
    response = response['result']
    for i in range(0, len(response)):
        uslugi.append(response[i]['fields']['usluga']['fields']['name'])
    return uslugi

id = abon_id("BILL0000139")
print(abon_usluga(str(id)))

