from utils.timer import set_interval

class ChatService:
    __connections = []

    def __init__(self, socketio):
        self.socketio = socketio
        self.socketio.on_event("connected", self.__connect, namespace="/chat")
        self.socketio.on_event("disconnected", self.__disconnect, namespace="/chat")
        self.socketio.on_event("is_connection", self.__is_connection, namespace="/chat")

        set_interval(self.__check_connections, 5)

    # Get all connections.
    def connections(self):
        return self.__connections
    
    # Get connection id by phone number.
    def connection_by_phone_number(self, phone_number):
        for connection in self.__connections:
            if connection["phoneNumber"] == phone_number:
                return connection
                
        return None
    
    # Response to a customer.
    def response(self, run_id, phone_number, message):
        connection = self.connection_by_phone_number(phone_number)

        if connection:
            self.socketio.emit("response", { 
                "id": run_id, 
                "phoneNumber": phone_number, 
                "content": message, 
                "type": "RECEIVE" 
            }, to=connection["id"], namespace="/chat")

    # Connect a new client.
    def __connect(self, connection):
        connectionFound = self.connection_by_phone_number(connection["phoneNumber"])

        if connectionFound:
            for conn in self.__connections:
                if conn["phoneNumber"] == connection["phoneNumber"]:
                    conn["id"] = connection["id"]
                    break
        else:
            self.__connections.append(connection)

        print("Connect: ", connection["phoneNumber"])

    # Disconnect a client.
    def __disconnect(self, connection):
        print("Disconnect: ", connection["phoneNumber"])

    # Is connection between server and client.
    def __is_connection(self, connection):
        print("Is connection: ", connection["phoneNumber"])

    # Check that each connection is available.
    def __check_connections(self):
        for connection in self.__connections:
            self.socketio.emit("check_connection", connection, to=connection["id"], namespace="/chat")