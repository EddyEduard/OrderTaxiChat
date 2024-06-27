import os

from openai import OpenAI
from dotenv import load_dotenv
from models.customer import Customer
from models.requests import Request

# Load environment variables.

load_dotenv()

# Connection to OpenAI API.

clientOpenAI = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Load assistant.

assistant = clientOpenAI.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))

# Create a thread for each customer.

def customer_thread(customerPhoneNumber):
    customerFound = Customer.objects(phone_number=customerPhoneNumber).first()

    if customerFound:
        threadFound = clientOpenAI.beta.threads.retrieve(customerFound.thread_id)

        if threadFound:
            return (threadFound, customerFound)
        else:
            thread = clientOpenAI.beta.threads.create()

            customerFound.thread_id = thread.id

            customerFound.save()

            return (thread, customerFound)
    else:
        thread = clientOpenAI.beta.threads.create()

        customer = Customer(thread_id=thread.id, phone_number=customerPhoneNumber)
        customer.save()

        return (thread, customer)
    
# Create a message.

def create_message(threadId, content):
    return clientOpenAI.beta.threads.messages.create(
        thread_id=threadId,
        role="user",
        content=content
    )
    
# Create a run to provide feedback on added messages.

def create_run(threadId, customerId, messageId):
    run = clientOpenAI.beta.threads.runs.create(
        thread_id=threadId,
        assistant_id=assistant.id
    )

    request = Request(customer_id=str(customerId), message_id=messageId, run_id=run.id)
    request.save()

    return run

# Get status of run.

def status_run(threadId, runId):
    run = clientOpenAI.beta.threads.runs.retrieve(
        run_id=runId,
        thread_id=threadId
    )

    return run.status

# Get the response message after run.

def get_response_message(threadId, runId):
    messages = clientOpenAI.beta.threads.messages.list(
        thread_id=threadId
    )

    for message in messages.data:
        if message.run_id == runId:
            return message

    return None