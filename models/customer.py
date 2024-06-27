from datetime import datetime
from mongoengine import Document, StringField, DateTimeField

class Customer(Document):
    thread_id = StringField(required=True, max_length=50)
    phone_number = StringField(required=True, max_length=15)
    created_date = DateTimeField(default=datetime.utcnow)
    meta = { "collection": "customers" }
