# Uncomment this to pass the first stage
from threading import Thread
import socket
import os

class WebServer:
    def __init__(self, host: int | str="localhost", port: int=4221) -> None:
        self.host = host 
        self.port = port 
        self.paths = ['']
        self.request_data = None

    def get_user_agent(self):
        return self.request_data['User-Agent']

    def create_server(self, run:bool = False) -> socket.socket:
        server = socket.create_server((self.host, self.port), reuse_port=True)

        if run:
            return self.run(server) 
        else:
            return server
        

    def http_code(self, http_path: str) -> str:
        http_path = (http_path.lstrip("GET").rstrip("HTTP/1.1")).strip()
        _str = ''

        match http_path:
            case s if http_path.startswith("/echo/"):
                http_path = http_path.lstrip("/echo/")
                _str = self.create_response(http_path)
            
            case s if http_path.startswith("/user-agent"):
                _str = self.create_response(self.get_user_agent())
                


            case "/":
                _str = "HTTP/1.1 200 OK\r\n\r\n"
        
            case _: 
                _str = "HTTP/1.1 404 Not Found\r\n\r\n"                 

        return _str

    def show_request(self, data: str) -> None:
        size = os.get_terminal_size()[0]
        print(f"\n{' Request Data ':=^{size}}")
        print(data)

    def _clean_request(self, data: str, return_dict = False) -> str | dict[str, str]:
        _dict = {}
        _str = ""

        http_request = (data[0].decode()).split("\r\n")
        _dict.update({"Request": http_request[0]})
        del http_request[0]

        for info in http_request:
            if ": " in info:
                key, value = info.split(": ", 1)
                _dict[key] = value 
        
        if return_dict:
            return _dict

        for k, v in _dict.items():
            _str += f"{k}: {v}\r\n"
        
        return _str


    def create_response(self, data:str) -> str:
        _str = 'HTTP/1.1 200\r\n'
        _str += "Content-Type: text/plain\r\n"
        _str += f"Content-Length:{len(data)}\r\n\r\n"
        _str += f"{data}\r\n\r\n"

        return _str

    def connection_handler(self, socket: socket.socket, log: bool = False) -> None:
        self.request_data = socket.recvmsg(1024)
        self.request_data = self._clean_request(self.request_data, return_dict=True)
        
        if log:
            self.show_request(self.request_data)

        socket.send(self.http_code(self.request_data["Request"]).encode())


    def run(self, server: socket.socket=None) -> None:
        
        if server is not None:
            while True:
                print("Logs from your program will appear here")
            
                socket, address = server.accept()

                thread = Thread(target = self.connection_handler, args=[socket])
                threads.append(thread)
                thread.start()

                for thread in threads:
                    thread.join()
                    print(f"{thread} closed.")


if __name__ == "__main__":
    webserver = WebServer()
    webserver.create_server(run=True)
