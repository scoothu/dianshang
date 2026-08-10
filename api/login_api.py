from api.base_api import BaseAPI


class LoginAPI(BaseAPI):
    def __init__(self):
        super().__init__()

    def login(self, username, password):
        url = "/api/login"
        data = {
            "username": username,
            "password": password
        }
        return self.post(url, json=data)

    def logout(self):
        url = "/api/logout"
        return self.post(url)

    def get_user_info(self):
        url = "/api/user/info"
        return self.get(url)