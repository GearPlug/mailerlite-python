# mailerlite-python

mailerlite-python is an API wrapper for MailerLite, written in Python

## Installing
```
pip install mailerlite-python
```

## Usage
```
from mailerlite.client import Client

client = Client('API_KEY')
```

### Subscribers

#### List Subscribers
```
subs = list_subscribers(params=None)
# Optional params (dict):
# filter[status] = Must be one of the possible statuses: active, unsubscribed, unconfirmed, bounced or junk.
# limit = Defaults to 25
# page = Defaults to 1
```
