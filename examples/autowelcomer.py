from argparse import ArgumentParser
from snapchat_agents import SnapchatAgent, Snap

class AutoWelcomerAgent(SnapchatAgent):
    def on_friend_add(self, friend):
        self.send_snap(friend, Snap.from_file("resources/auto_welcome.png"))

if __name__ == '__main__':
    parser = ArgumentParser("Auto-Welcomer Agent")
    parser.add_argument('-u', '--username', required = True, type=str, help = "Username of the account to run the agent on")
    parser.add_argument('-p', '--password', required = True, type=str, help = "Password of the account to run the agent on")

    args = parser.parse_args()

    agent = AutoWelcomerAgent(args.username, args.password)
    agent.listen()
