import socket


def main():
        host = '192.168.1.120'
        port = 4040

        mySocket = socket.socket()
        mySocket.connect((host, port))

        message = input(" -> ")

        while message != 'q':
                mySocket.send(message.encode())
                data = mySocket.recv(1024).decode()

                print('Received from server: ' + data)

                message = input(" -> ")

        mySocket.close()

if __name__ == '__main__':
    main()



