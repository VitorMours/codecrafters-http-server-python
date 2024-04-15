# Uncomment this to pass the first stage
import socket
import re
import os

class WebServer:
    def __init__(self, host: int | str="localhost", port:int=4221) -> None:
        self.host = host 
        self.port = port 
        self.server = None
        self.paths = ['']
        

    def create_server(self, not_run:bool) -> socket.socket:
        self.server = socket.create_server((self.host, self.port), reuse_port=True)

        if not_run:
            return self.server 
        else:
            self.run(self.server)
        

    def http_code(self, http_path: str) -> str:
        http_path = (http_path.lstrip("GET").rstrip("HTTP/1.1")).strip()
        _str = ''

        match http_path:
            case s if http_path.startswith("/echo/"):
                http_path.lstrip("/echo/")
                _str = "HTTP/1.1 200\r\n"
                _str += "Content-Type: text/plain\r\n" 
                _str += f"Content-Length:{len(http_path)} \r\n\r\n"
                _str += f"{http_path}\r\n\r\n"


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
            else:
                print(f"Ignorando linha mal formatada: {info}")
        
        if return_dict:
            return _dict

        for k, v in _dict.items():
            _str += f"{k}: {v}\r\n"
        
        return _str


    def create_response(self, status:int) -> None:
        pass

    def run(self, server: socket.socket=None) -> None:
        
        if self.server is None:
            self.server = self.create_server()
        
        print("Logs from your program will appear here")
        while True:
            socket, address = self.server.accept()
             
            data = socket.recvmsg(1024)
            data = self._clean_request(data, return_dict=True)

            socket.send(self.http_code(data["Request"]).encode())

#            socket.send(response)





def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
   
    server_socket = socket.create_server(("localhost", 4221), reuse_port = True)
    print(f"\n\n{type(server_socket)}\n\n")
    while True:
        sock, addr = server_socket.accept() # wait for client
        print(sock, addr)
        
        # Pegando os dados recebidos, e tentando enetneder eles de maneira mais organizada
        data = sock.recvmsg(1024)
        message = data[0]
        print(f"{' Message Data ':=^80}\n{data}")
        print("\n" + message.decode())
        print(bytes(message))
        
        
        http_message = (message.decode()).split("\r\n")[0:3]
#        print(http_message)
       
        http_path = (http_message[0].split())[1]
#        print(http_path)
#        print(http_path.encode())
        status_message = "HTTP/1.1 200 OK\r\n"
            
        
            

        
        if http_path.startswith("/echo/"):
            http_path = http_path.strip()
#            print(http_path)
            status_message += 'Content-Type: text/plain\r\n'
            path_message = http_path.lstrip('/echo/')
            status_message += f'Content-Length: {len(path_message)}\r\n'
            status_message += f'\r\n\r\n{path_message}'



        print(status_message)
        sock.send(status_message.encode())

if __name__ == "__main__":
    webserver = WebServer()
    webserver.create_server(not_run=False)
    #main()
