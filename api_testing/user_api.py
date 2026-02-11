from base_request import BaseRequest

class UserAPI(BaseRequest):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.endpoint = 'user'
    
    def create_user(self, user_data):
        response = self.post(self.endpoint, '', user_data)
        return response
    
    def get_user(self, username):
        response = self.get(self.endpoint, username)
        return response
    
    def update_user(self, username, user_data):
        response = self.put(self.endpoint, username, user_data)
        return response
    
    def delete_user(self, username):
        response = self.delete(self.endpoint, username)
        return response