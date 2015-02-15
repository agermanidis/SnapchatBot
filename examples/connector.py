from argparse import ArgumentParser
from snapchat_agents import SnapchatAgent, Snap

class ConnectorAgent(SnapchatAgent):
    def initialize(self):
        self.connections = []
        self.unconnected = None

    def connect(self, u1, u2):
        self.log("New Connection: %s <-> %s" % (u1, u2))
        self.connections.append((u1, u2))

    def on_friend_add(self, friend):
        if self.unconnected is not None:
            self.connect(friend, self.unconnected)
            self.unconnected = None
        else:
            self.unconnected = friend

    def on_friend_delete(self, friend):
        other = self.find_connection(friend)

        if self.unconnected is not None:
            self.connect(other, self.unconnected)
            self.unconnected = None

        else:
            self.unconnected = other

    def find_connection(self, username):
        for (u1, u2) in self.connections:
            if u1 == username:
                return u2
            elif u2 == username:
                return u1

    def on_snap(self, sender, snap):
        connection = self.find_connection(sender)

        if connection:
            self.send_snap([connection], snap)
        else:
            self.send_snap([sender], Snap.from_file("resources/connector_fail.png"))

if __name__ == '__main__':
    parser = ArgumentParser("ConnectorAgent Agent")
    parser.add_argument('-u', '--username', required = True, type=str, help = "Username of the account to run the agent on")
    parser.add_argument('-p', '--password', required = True, type=str, help = "Password of the account to run the agent on")

    args = parser.parse_args()

    agent = ConnectorAgent(args.username, args.password)
    agent.listen(timeout = 5)
