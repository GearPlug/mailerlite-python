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
subs = client.list_subscribers(params=None)
# Optional params (dict):
# filter[status] = Must be one of the possible statuses: active, unsubscribed, unconfirmed, bounced or junk.
# limit = Defaults to 25
# page = Defaults to 1
```
#### Create Subscriber
```
subscriber = {
    "email": "juankrios15@gmail.com",
    "fields": {
        "name": "Carlos",
        "last_name": "Burgos",
        "city": "Bogotá",
    }
}
sub = client.create_subscribers(subscriber)
```
#### List Groups
```
groups = client.list_groups(params=None)
# Optional params (dict):
# filter[name] = Returns partial matches
# limit = An account can have at most a 250 groups
# page = Defaults to 1
# sort = Can be one of: name, total, open_rate, click_rate, created_at. Defaults to ascending order; prepend (-)
```

### Webhooks
#### List all webhooks

```
webhooks = client.list_webhooks()
```
#### Create webhook

```
webhook = {
    "name": "first webhook",
    "events": ["subscriber.created"],
    "url": "http://www.cartwright.info/eligendi-soluta-corporis-in-quod-ullam"
}
webhook_created = client.create_webhook(webhook)
```