import requests

from mailerlite.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    url = 'https://connect.mailerlite.com/api/'
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    def __init__(self, api_key):
        self.headers.update(Authorization=f"Bearer {api_key}")
    
    def list_subscribers(self, params=None):
        """
        Params:
        filter[status] = Must be one of the possible statuses: active, unsubscribed, unconfirmed, bounced or junk.
        limit = Defaults to 25
        page = Defaults to 1
        """
        return self.get('subscribers', params=params)
    
    def get(self, endpoint, params=None):
        response = self.request('GET', endpoint, params=params)
        return self.parse(response)
    
    def request(self, method, endpoint, params=None, data=None, headers=None, json=True):
        _headers = self.headers
        if headers:
            _headers.update(headers)
        kwargs = {}
        if json:
            kwargs['json'] = data
        else:
            kwargs['data'] = data
        return requests.request(method, self.url + endpoint, params=params, headers=_headers, **kwargs)
    
    def parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
