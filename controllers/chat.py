from flask import render_template, request
from services.assistant import customer_thread, create_message, create_run

from models.customer import Customer

# Load chat page.

def index():
    return render_template("chat.html")

# Check the phone number if it already exists.

def check_phone_number():
    customerPhoneNumber = request.args.get("phoneNumber")

    customer = Customer.objects(phone_number=customerPhoneNumber).first()

    if customer:
        return { "status": 403, "message": "Phone number is in use!" }, 403

    return { "status": 200, "message": "Phone number not in use!" }

# Receive messages from customers.

def send_message():
    customerMessage = request.json["content"]
    customerPhoneNumber = request.json["phoneNumber"]

    print(f'MeridianTaxiAssistant << {customerPhoneNumber} : {customerMessage}')

    (thread, customer) = customer_thread(customerPhoneNumber)
    
    message = create_message(thread.id, customerMessage)

    create_run(thread.id, customer.id, message.id)

    return { "status": 200, "message": "Message sent successfully!" }

