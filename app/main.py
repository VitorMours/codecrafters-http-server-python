# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        sock, addr = server_socket.accept() # wait for client
        print(sock, addr)
        
        # Pegando os dados recebidos, e tentando enetneder eles de maneira mais organizada
        data = sock.recvmsg(1024)
        message = data[0]
        print(data)
        print("\n" + message.decode())
        
        
        http_message = (message.decode()).split("\n")[0:3]
        print(http_message)
       
        http_path = (http_message[0].split())[1]
        print(http_path)
       
        match http_path:
            case "/":
                status_message = "HTTP/1.1 200 OK\r\n\r\n"

            case _: 
                status_message = "HTTP/1.1 404 Not Found\r\n\r\n"



        print(status_message)
        sock.send(status_message.encode())

if __name__ == "__main__":
    main()
