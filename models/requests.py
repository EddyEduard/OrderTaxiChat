from datetime import datetime
from mongoengine import Document, StringField, DateTimeField

class Request(Document):
    customer_id = StringField(required=True)
    message_id = StringField(required=True, max_length=50)
    run_id = StringField(required=True, max_length=50)
    created_date = DateTimeField(default=datetime.utcnow)
    meta = { "collection": "requests" }
