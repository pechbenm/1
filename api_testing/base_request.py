import requests
import pprint

class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        if request_type == 'GET':
            response = requests.get(url)
        elif request_type == 'POST':
            response = requests.post(url, json=data)  
        elif request_type == 'PUT':
            response = requests.put(url, json=data)   
        elif request_type == 'DELETE':
            response = requests.delete(url)
        else:
            response = requests.patch(url, json=data)

        print(f' {request_type} запрос: {url}')
        print(f' cтатус: {response.status_code}')
        # pprint.pprint(f'{request_type} example')
        # pprint.pprint(response.url)
        # pprint.pprint(response.status_code)
        # pprint.pprint(response.reason)
        # pprint.pprint(response.text)
        # if response.text:  # Проверяем что ответ не пустой
        #     pprint.pprint(response.json())
        # pprint.pprint('**********')
        
        return response

    def get(self, endpoint, endpoint_id, expected_error=False):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response

    def post(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'POST', data=body)
        return response

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response
    
    def put(self, endpoint, endpoint_id, body, expected_error=False):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'PUT', data=body, expected_error=expected_error)
        return response