# OrderTaxiChat

OrderTaxiChat is an app for ordering a taxi through conversation with a chatbot. A ChatGPT-based assistant from OpenAI was used to create the chatbot. Which was trained with some instructions in the area of ordering a taxi, taking the address from the customer and registering a new order in the system.

## Technologies

Below is a list of all the technologies used to develop the app. They are structured by categories.

**Frontend**
   - HTML
   - CSS
   - JavaScript
   - **Libraries**
     - Bootstrap
     - Font Awesome 4 Icons
     - jQuery

**Backend**
   - Python
   - Flask

**Databases**
   - MongoDB

**Cloud**
   - [OpenAI Platform](https://platform.openai.com/docs/overview)

## Run & Build commands

The application is developed using the Flask framework.

Before executing any command, we must make sure that the packages are installed, otherwise we must install them using this command:
```
pip install -r requirements.txt
```

To run the application in the development mode use this command:
```
python server.py
```

## Management of Folder & Files

The project is structured as follows:

- [Assets](https://github.com/EddyEduard/OrderTaxiChat/tree/main/assets) used for storing static files (CSS, JS, images);
- [Controllers](https://github.com/EddyEduard/OrderTaxiChat/tree/main/controllers) used to control actions in the application;
- [Helpers](https://github.com/EddyEduard/OrderTaxiChat/tree/main/helpers) used to store useful functions;
- [Models](https://github.com/EddyEduard/OrderTaxiChat/tree/main/models) are used for modeling database tables;
- [Routers](https://github.com/EddyEduard/OrderTaxiChat/tree/main/routers) contains all routers between controllers and models;
- [Services](https://github.com/EddyEduard/OrderTaxiChat/tree/main/services) contains the main chat and chatbot services;
- [Templates](https://github.com/EddyEduard/OrderTaxiChat/tree/main/templates) contains the web pages;
- [Utils](https://github.com/EddyEduard/OrderTaxiChat/tree/main/utils) containing some useful functions.

## Features & Functionalities

The chatbot can execute the next tasks:

1. Have a friendly and decent conversation with the customer;
2. Ask for the address of the order;
3. Ask about the date and time of the taxi dispatch;
4. To ask about method of payment;
5. Record the order in the system.

## Database

The database used for data storage is [MongoDB](https://www.mongodb.com/).

## System Diagram

### Entity Relationship Diagram

```mermaid
erDiagram
    CUSTOMER {
        string id PK
        string(10) phone_number
        ADDRESS address
        string thread_id
        date created_date
    }

    REQUEST {
        string id PK
        string cutomer_id HK
        string message_id
        string run_id
        date created_date
    }

    ADDRESS {
        string country
        string state
        string city
        string line1
        string line2
        string postal_code
    }

     USER ||--|| ADDRESS : "has address"
     USER ||--o{ REQUEST : "has requests"
```

## License
Distributed under the MIT License. See [MIT](https://github.com/EddyEduard/OrderTaxiChat/blob/master/LICENSE) for more information.

## Contact
EddyEduard - [eduard_nicolae@yahoo.com](mailTo:eduard_nicolae@yahoo.com)
\
Project link - [https://github.com/EddyEduard/OrderTaxiChat](https://github.com/EddyEduard/OrderTaxiChat.git)
