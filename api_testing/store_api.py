from base_request import BaseRequest

class StoreAPI(BaseRequest):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.endpoint = 'store'

    def get_inventory(self):
        url = f'{self.base_url}/{self.endpoint}/inventory'
        response = self._request(url, 'GET')
        return response
    
    def get_order(self, order_id):
        response = self.get(self.endpoint, f'order/{order_id}')
        return response
    
    def create_order(self, order_data):
        response = self.post(self.endpoint, 'order', order_data)
        return response
    
    def delete_order(self, order_id):
        response = self.delete(self.endpoint, f'order/{order_id}')
        return response