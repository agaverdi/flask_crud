import requests
from http import HTTPStatus
import json
from pprint import pprint
def response_get():
    response_get = requests.get('http://127.0.0.1:5000/animals')

    if response_get.status_code == HTTPStatus.OK:
        return response_get.json()
    else:
        return {"result":False}
    



def get_animal_id(id):
    
    response=requests.get(f'http://127.0.0.1:5000/animals/{id}')
     
    if response.status_code==HTTPStatus.OK:
        return response.json()
    else:
        return "animal not found"


def post_animal():
    response_post=requests.post('http://127.0.0.1:5000/animals', json={"name":"sican"})


def put_animal_id(id):
    data={'id':id,'name':'yeni at'}
    pprint(json.dumps(data))
    if data.id==id:
        response=requests.put(f'http://127.0.0.1:5000/animals/{id}' ,json=json.dumps(data))
     
        if response.status_code== HTTPStatus.OK:
            return response.json()
        else:
            return "isdemedi"



def delete_animal_id(id):
    response_delete=requests.delete(f"http://127.0.0.1:5000/animals/{id}")

    return response_delete
        # print(response_delete.request.body)

# pprint(post_animal())
pprint(response_get())
pprint(get_animal_id(10))
# pprint(put_animal_id(6))
# pprint(delete_animal_id(16))
# pprint(response_get.json())
# pprint("salam baki")