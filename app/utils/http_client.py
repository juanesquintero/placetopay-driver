from requests import get, post, put, patch, delete
from flask import flash

class HttpClient():

    __instance = None

    @staticmethod
    def get_instance():
        return HttpClient.__instance

    #  Singleton definition
    def __init__(self, api_path, headers=None):
        if HttpClient.__instance is not None:
            raise Exception('The http API client can only be instance once!')
        self.api_path = api_path
        self.headers = headers
        HttpClient.__instance = self

    def set_headers(self, headers):
        self.headers = headers

    def request_params(self, endpoint, body=None):
        return dict(
            url=self.api_path + endpoint,
            headers=self.headers,
            json=body
        )

    @staticmethod
    def check_response(res):
        try:
            body = res.json()
        except Exception as e:
            body = res.text
        status = res.status_code
        if (str(status)[0] in ['2', '3']):
            return body
        return flash(f'ERROR in API call: {body}', 'danger')

    def get(self, endpoint):
        res = get(**self.request_params(endpoint))
        return self.check_response(res)

    def post(self, endpoint, body):
        res = post(**self.request_params(endpoint, body))
        return self.check_response(res)

    def put(self, endpoint, body):
        res = put(**self.request_params(endpoint, body))
        return self.check_response(res)

    def patch(self, endpoint, body):
        res = patch(**self.request_params(endpoint, body))
        return self.check_response(res)

    def delete(self, endpoint):
        res = delete(**self.request_params(endpoint))
        return self.check_response(res)
        