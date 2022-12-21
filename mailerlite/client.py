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

    def fetch_subscriber(self, reference):
        """
        Params:
        reference = Email or ID
        """
        return self.get(f'subscribers/{reference}')

    def create_subscriber(self, data):
        """
        Request:
            email: Valid email address (REQUIRED)
            fields (object): Object keys must correspond to default or custom fields
            groups (array): array must contain existing group ids.
            status: Can be one of the following: active, unsubscribed, unconfirmed, bounced, junk
            subscribed_at: Must be a valid date in the format yyyy-MM-dd HH:mm:ss
            ip_address: Must be a valid ip address
        """
        return self.post('subscribers', data=data)

    def activate_subscriber(self, subscriber_id):
        """
        Unsubscribe user subscribed.
        """
        return self.post(f'subscribers/{subscriber_id}/subscribe')

    def unsubscribe_subscriber(self, subscriber_id):
        """
        Unsubscribe user subscribed.
        """
        return self.post(f'subscribers/{subscriber_id}/unsubscribe')

    def delete_subscriber(self, subscriber_id):
        """
        Unsubscribe user subscribed.
        """
        return self.delete(f'subscribers/{subscriber_id}')

    def assign_to_group(self, subscriber_id, group_id):
        """
        Assign specific user/subscriber to group
        """
        return self.post(f'subscribers/{subscriber_id}/groups/{group_id}')

    def list_subscriber_fields(self):
        """
        List Subscriber Default and Custom Fields
        """
        return self.get(f'fields')

    def list_groups(self, params=None):
        """
        Params:
        limit = An account can have at most a 250 groups
        page = Defaults to 1
        filter[name] = Returns partial matches
        sort = Can be one of: name, total, open_rate, click_rate, created_at. Defaults to ascending order; prepend -, 
               e.g. -total for descending order
        """
        return self.get('groups', params=params)

    def list_webhooks(self):
        """
        List all webhooks
        """
        return self.get(f'webhooks')

    def create_webhook(self, data):
        """
        Request
        name: Not Required
        events: (array) Must be one of the events in 'available events' list
        url: connecting endpoint
        """
        return self.post('webhooks', data=data)

    def delete_webhook(self, webhook_id):
        """
        Delete specific webhook using its ID
        """
        return self.delete(f'webhooks/{webhook_id}')

    def get(self, endpoint, params=None):
        response = self.request('GET', endpoint, params=params)
        return self.parse(response)

    def post(self, endpoint, params=None, data=None, headers=None, json=True):
        response = self.request('POST', endpoint, params=params, data=data, headers=headers, json=json)
        return self.parse(response)

    def delete(self, endpoint, params=None):
        response = self.request('DELETE', endpoint, params=params)
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
        if 'Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']:
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
