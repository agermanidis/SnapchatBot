from argparse import ArgumentParser
from snapchat_agents import SnapchatAgent

class ConnectorAgent(SnapchatAgent):
    def initialize(self):
        self.connections = []
        self.unlinked = None

    def on_friend_add(self, friend):
        if self.unlinked is not None:
            self.connections.append( (friend, self.unlinked) )
            self.unlinked = None
        else:
            self.unlinked = friend

    def find_connection(self, username):
        for (u1, u2) in self.links:
            if u1 == username:
                return u2
            elif u2 == username:
                return u1

    def on_snap(self, sender, snap):
        connection = self.find_connection(sender):
        if connection:
            self.send_snap([connection], snap)
        else:
            self.send_snap([sender], Snap.from_file("resources/auto_welcome.png"))

if __name__ == '__main__':
    parser = ArgumentParser("ConnectorAgent Agent")
    parser.add_argument('-u', '--username', required = True, type=str, help = "Username of the account to run the agent on")
    parser.add_argument('-p', '--password', required = True, type=str, help = "Password of the account to run the agent on")

    args = parser.parse_args()

    agent = ConnectorAgent(args.username, args.password)
    agent.listen()
