# Uncomment this to pass the first stage



from http_server import HttpWebServer
from threading import Thread
import socket
import os




if __name__ == "__main__":
    webserver = HttpWebServer(log=True)
    webserver.create_server(run=True)
