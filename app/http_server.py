import os
import socket 
import sys
from threading import Thread 
from request import Request

class HttpWebServer:
    def __init__(self, host: int | str="localhost", port: int=4221, log: bool = False) -> None:
        self.host = host 
        self.port = port 
        self.files = {}
        self.request_data = None
        self.log = log
    
    
    def get_user_agent(self):
        """
        Getter to the user agent used to access the server. 

        Returns
        -------
            self.request_data['User-Agent']: str
        """
        return self.request_data['User-Agent']

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
    
                print(sys.argv)                


                _str =  self.create_response(_path) 
            




            case "/user-agent":
                self.create_response("text/plain", self.get_user_agent())


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
        _str = 'HTTP/1.1 200\r\n'
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





# Auxiliar Class



