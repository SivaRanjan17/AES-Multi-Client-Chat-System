"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import AES

key = b'master key'
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        message = "Greetings from the cave! Now type your name and press enter!"
        message = message.encode('UTF-8')
        ciphertext = AES.encrypt(key, message)
        client.send(ciphertext)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ)
    name = AES.decrypt(key, name).decode("utf-8")
    
    welcome = '\nWelcome %s! If you ever want to quit, type {quit} to exit.' % name
    message = welcome.encode('UTF-8')
    ciphertext = AES.encrypt(key, message)
    client.send(ciphertext)
   # msg = "%s has joined the chat!" % name
    #broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        message = client.recv(BUFSIZ)
        message = AES.decrypt(key, message).decode("utf-8")
        if message != "{quit}":
            broadcast(message, name+": ")
        else:
            client.close()
            del clients[client]
            if bool(clients) == False:
                SERVER.close()
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    message = prefix + msg
    ciphertext = AES.encrypt(key, message)
    for sock in clients:
        sock.send(ciphertext)

        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()