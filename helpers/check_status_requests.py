import threading

from services.assistant import status_run, get_response_message
from models.customer import Customer
from models.requests import Request

# Check status of sent requests.

def check_status_requests(chat_service, connections):
    requests = Request.objects()
    recall = requests.count() > 0

    for request in requests:
        customer = Customer.objects(id=request.customer_id).first()

        if customer:
            status = status_run(customer.thread_id, request.run_id)

            if status == "completed":
                response = get_response_message(customer.thread_id, request.run_id)
                message = response.content[0].text.value

                request.delete()
                
                chat_service.response(request.run_id, customer.phone_number, message)

                print(f'MeridianTaxiAssistant >> {customer.phone_number} : {message}')
            elif status in ["cancelling", "cancelled", "failed", "completed", "expired"]:
                request.delete()

    if recall:
        check_status_requests(chat_service, connections)

# Handle insert changes.

def handle_requests(client_DB, chat_service, connections):
    def lookup():
        changes = client_DB.MeridianTaxiChat.requests.watch([{
            "$match": {
                "operationType": { "$in": ["insert"] }
            }
        }])
        
        for _ in changes:
            check_status_requests(chat_service, connections)

    thread = threading.Thread(target=lookup)
    thread.daemon = True
    thread.start()