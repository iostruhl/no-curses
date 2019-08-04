import sys
from sys import stdin, exit
from time import sleep
from util.card import Card
from util.graphics import GraphicsBoard
import shutil
from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
    def __init__(self, host, port, name = "ANON", sort_hand_ascending = False):
        self.Connect((host, port))
        print("Oh Hell client started")
        print("Ctrl-C to exit")
        self.name = name
        self.sort_hand_ascending = sort_hand_ascending
        # get a nickname from the user before starting
        connection.Send({"action": "name", "name": name})

    def Loop(self):
        connection.Pump()
        self.Pump()

    #################
    ### Built-ins ###
    #################

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_server_name(self, data):
        print("Server set name to", data['name'])
        self.name = data['name']
        connection.Send({
                'action': "ready",
                'name': self.name
            })

    def Network_names(self, data):
        print("*** users:", ', '.join([p for p in data['names']]), "***")

    def Network_pause(self, data):
        print("*** USER HAS DISCONNECTED, FATAL ***")
        exit(1)

    def Network_update(self, data):

    def Network_end_game(self, data):

if __name__ == "__main__":
    if len(sys.argv) not in [3,4]:
        print("Usage:", sys.argv[0], "host:port name [--sort_hand_ascending]")
        print("e.g.", sys.argv[0], "localhost:8080 Isaac")
    else:
        size = shutil.get_terminal_size()
        assert (size.columns >= 181 and size.lines >= 58), \
            "Resize terminal to at least 181x58"
        host, port = sys.argv[1].split(":")
        c = Client(host, int(port), name = sys.argv[2],
                   sort_hand_ascending = (len(sys.argv) == 4))
        while 1:
            c.Loop()
            sleep(0.001)
