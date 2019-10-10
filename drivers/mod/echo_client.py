import socket


def main():
        host = '192.168.0.49'
        port = 1717

        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect((host, port))

        # message = input(" -> ")

        # while message != 'q':
                # mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()
        print('Received from server: ' + data)

                # message = input(" -> ")

        mySocket.close()


if __name__ == '__main__':
    main()



