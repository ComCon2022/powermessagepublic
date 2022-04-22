from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
try:
    import cryptocode
except:
    print("Fatal Error! Failed to get required libs. Error note: Please install Cryptocode using 'pip install cryptocode'")
    os.system('pause')

print("WARNING! THIS IS A DEVELOPER BUILD AND MAY NOT BE STABLE!")

users = []
passwords = []

def broadcast(amsg):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(amsg, "utf8"))

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        global client_address
        global addresses
        client, client_address = SERVER.accept()
        print("%s:%s is attempting to connect." % client_address)
        passcheck = False
        passsucceed = False
        while passcheck == False:
            if client.recv(BUFSIZ).decode("utf8") == PASS:
                client.send(bytes("true", "utf8"))
                passcheck = True
                passsucceed = True
            else:
                print("%s:%s has failed authentication." % client_address)
                client.send(bytes("false", "utf8"))
                client.close()
                break
        while passsucceed == True:
            addusrcachesplitarry = client.recv(BUFSIZ).decode("utf8")
            if "SP" in addusrcachesplitarry:
                print("wr")
                addusrcachesplitarrysplited = addusrcachesplitarry.split(":")
                print("wr")
                print(addusrcachesplitarrysplited)
                users.append(addusrcachesplitarrysplited[1])
                passwords.append(addusrcachesplitarrysplited[2])
                print(users)
                print(passwords)
                addresses[client] = client_address
                print("%s:%s has connected." % client_address)
                Thread(target=handle_client, args=(client, addusrcachesplitarrysplited[1],)).start()
                passsucceed = False
            elif "LN" in addusrcachesplitarry:
                addusrcachesplitarrysplited = addusrcachesplitarry.split(":")
                print(addusrcachesplitarrysplited)
                if addusrcachesplitarrysplited[1] in users:
                    if addusrcachesplitarrysplited[2] == passwords[users.index(addusrcachesplitarrysplited[1])]:
                        client.send(bytes("authsucceed", "utf8"))
                        addresses[client] = client_address
                        print("%s:%s has connected." % client_address)
                        Thread(target=handle_client, args=(client, addusrcachesplitarrysplited[1],)).start() 
                        passsucceed = False
                    else:
                        client.send(bytes("wrongpasscode", "utf8"))
                        client.close()
                        passsucceed = False

                else:
                    client.send(bytes("nouserfound", "utf8"))
                    client.close()
                    passsucceed = False

def handle_client(client, name):  # Takes client socket as argument.
    """Handles a single client connection."""
    welcome = 'Welcome , to terminate connection type /quit.'
    ewelcome = cryptocode.encrypt(welcome, PASS)
    client.send(bytes(ewelcome, "utf8"))
    msg = "%s has joined the server." % name
    msg = cryptocode.encrypt(msg, PASS)
    broadcast(msg)
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFSIZ).decode("utf8")
            decryptedmsg = str(cryptocode.decrypt(msg, PASS))
            print(decryptedmsg)
            if "gb:/quit" == decryptedmsg:
                client.close()
                del clients[client]
                left = "%s has left the server." % name
                leftmsg = cryptocode.encrypt(left, PASS)
                broadcast(leftmsg)
                print("%s has terminated connection with server." % name)
                break
            elif decryptedmsg.startswith('fr:'):
                friendsplit = decryptedmsg.split(":")
                if friendsplit[1] in users:
                    client.send(bytes(cryptocode.encrypt("User Found", PASS), "utf8"))
                else:
                    client.send(bytes(cryptocode.encrypt("User Not Found", PASS), "utf8"))
            elif decryptedmsg.startswith('gb:'):
                dmsg = cryptocode.decrypt(msg, PASS)
                pdgmsg = dmsg.split(":")
                pmsg = pdgmsg[1]
                ename = str(name)
                broadcastmsg = cryptocode.encrypt((ename+": "+pmsg), PASS)
                strbroadcast = str(broadcastmsg)
                print(cryptocode.decrypt(strbroadcast, PASS))
                broadcast(strbroadcast)
        except OSError:
            break

clients = {}
addresses = {}
global PASS
global LSERVER
HOST = "0.0.0.0"
PORT = int(input("Enter Port, Default is 33000: "))
PASS = input('Enter Server Password: ')
while not PASS:
    PASS = input('Server Password is Required: ')
LANS = input('Y/N, Enable Invisible Mode?: ')
if LANS == "N":
    LANP = 33500
    if LANP == PORT:
        PORT = PORT + 1
    LADDR = (HOST, LANP)
    LSERVER = socket(AF_INET, SOCK_DGRAM)
    LSERVER.bind(LADDR)
BUFSIZ = 4096
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("---------------------------------")                            
    print("ComCon Powermessage Server")
    print("---------------------------------")
    print("Default IP:")
    print("127.0.0.1")
    print("Port:")
    print(PORT)
    if LANS == "N":
        print("LAN Discovery Port:")
    print("---------------------------------")
    print("Awaiting Connections")
    if LANS == "N":
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        GUI_THREAD = Thread()
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    else:
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    SERVER.close()