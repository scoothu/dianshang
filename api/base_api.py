import requests
from utils.config import ConfigManager
from utils.logger import Logger


class BaseAPI:
    def __init__(self):
        self.base_url = ConfigManager().get_base_url()
        self.timeout = ConfigManager().get_timeout()
        self.logger = Logger()
        self.session = requests.Session()
        self.token = None

    def set_token(self, token):
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, url, params=None, headers=None):
        try:
            full_url = self.base_url + url
            self.logger.info(f"GET request: {full_url}, params: {params}")
            response = self.session.get(full_url, params=params, headers=headers, timeout=self.timeout)
            self.logger.info(f"GET response status: {response.status_code}, data: {response.text[:200]}")
            return response
        except Exception as e:
            self.logger.error(f"GET request error: {e}")
            raise

    def post(self, url, data=None, json=None, headers=None):
        try:
            full_url = self.base_url + url
            self.logger.info(f"POST request: {full_url}, data: {data}, json: {json}")
            response = self.session.post(full_url, data=data, json=json, headers=headers, timeout=self.timeout)
            self.logger.info(f"POST response status: {response.status_code}, data: {response.text[:200]}")
            return response
        except Exception as e:
            self.logger.error(f"POST request error: {e}")
            raise

    def put(self, url, data=None, json=None, headers=None):
        try:
            full_url = self.base_url + url
            self.logger.info(f"PUT request: {full_url}, data: {data}, json: {json}")
            response = self.session.put(full_url, data=data, json=json, headers=headers, timeout=self.timeout)
            self.logger.info(f"PUT response status: {response.status_code}, data: {response.text[:200]}")
            return response
        except Exception as e:
            self.logger.error(f"PUT request error: {e}")
            raise

    def delete(self, url, params=None, headers=None):
        try:
            full_url = self.base_url + url
            self.logger.info(f"DELETE request: {full_url}, params: {params}")
            response = self.session.delete(full_url, params=params, headers=headers, timeout=self.timeout)
            self.logger.info(f"DELETE response status: {response.status_code}, data: {response.text[:200]}")
            return response
        except Exception as e:
            self.logger.error(f"DELETE request error: {e}")
            raise