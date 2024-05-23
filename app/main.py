# Uncomment this to pass the first stage
#from http_server import HttpWebServer
from threading import Thread
import socket
import sys
import os

class Request:
    def __init__(self, http_method: str, path: str, http_version: str) -> None:
        self._http_method = http_method 
        self._path = path 
        self._http_version = http_version 


    @property
    def http_method(self):
        """The http_method property."""
        return self._http_method
    
    @http_method.setter
    def http_method(self, value):
        self._http_method = value


    @property
    def path(self):
        """The path property."""
        return self._path
    
    @path.setter
    def path(self, value):
        self._path = value
        

    @property
    def http_version(self):
        """The http_version property."""
        return self._http_version


    @http_version.setter
    def http_version(self, value):
        self._http_version = value


 

    def __str__(self) -> None:
        str = f'Http Method: {self._http_method}\n'
        str += f'Request path: {self._path}\n'
        str += f'Http Version: {self._http_version}'

        return str


    def has_directory(self, directory: str, first_directory: bool = False) -> bool:
        
        if first_directory:
            if self.path.startswith(directory):
                return True

        if directory in self.path:
            return True

        return False


class HttpWebServer:
    def __init__(self, host: int | str="localhost", port: int=4221, log: bool = False) -> None:
        self.host = host 
        self.port = port 
        self.files = {}
        self.request_data = None
        self.log = log
    
    
    def create_server(self, run:bool = False) -> socket.socket:
        """ 
        Responsible function to create the server and run the same. 
        
        Parameters 
        ----------
        run: bool 
            Defines if the server gonna run the time it's created, or not.    

        Returns
        -------
        server: socket.server or None: 
            Returns a web server with the socket library, or return nothing, depends
            if it's in automatic running, or not.
        """
        server = socket.create_server((self.host, self.port), reuse_port=True)

        if run:
            self.run(server) 
        else:
            return server
        

    def http_code(self, http_path: str) -> str:
       
        request = Request(*http_path.split())
        _str = ''

        
        
        match request.path:

            case s if request.has_directory("/echo/", first_directory=True):
                _path = request.path.lstrip("/echo/")
                _str = self.create_response("text/plain", _path)
            
            case s if request.has_directory("/files/"):
                
                _path = request.path.lstrip("/files/")
    
                directory = sys.argv[2] 
                file_path = request.path[7:]
                
                try:
                    with open(f"{directory}{file_path}") as file:
                        _path = file.read()
 
                        _str =  self.create_response("application/octet-stream", _path) 
                except FileNotFoundError:
                    _str = "HTTP/1.1 404 Not Found\r\n\r\n"


            case "/user-agent":

                print(f"\n\n{request}")

                _type = "text/plain"
                _str = self.create_response(_type, self.request_data["User-Agent"])


            case "/":
                _str = "HTTP/1.1 200 OK\r\n\r\n"
        
            case _: 
                _str = "HTTP/1.1 404 Not Found\r\n\r\n"                 

        return _str

    def show_request(self, data: str | dict[str, str]) -> None:
        """
        Function to show the request in a better visualization in the terminal, normally the 
        request is to visualization after the cleaning, but this can be modified.
        
        Parameters 
        ----------
        data: str or dict[str, str]
            String or -- most common -- dictionary of strings with information of the request 
            to be show
    
        Returns
        ------- 
        None
        """
        
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


    def create_response(self, type:str, data:str) -> str:
        _str = 'HTTP/1.1 200 OK\r\n'
        _str += f"Content-Type: {type}\r\n"
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
        """
        Function to run the server  

        """
            


        threads = [] 
        if server is not None:
            try:
                while True:
                    print("Logs from your program will appear here")
            
                    socket, address = server.accept()
                    thread = Thread(target = self.connection_handler, args=[socket, self.log])
                    threads.append(thread)
                    thread.start()

            finally:
                for thread in threads:
                    thread.join(timeout=15)
                    print(f"{thread} closed.")






if __name__ == "__main__":
    webserver = HttpWebServer()
    webserver.create_server(run=True)
