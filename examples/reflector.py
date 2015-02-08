from argparse import ArgumentParser
from snapchat_agents import SnapchatAgent

class ReflectorAgent(SnapchatAgent):
    def on_snap(self, sender, snap):
        self.send_snap([sender], snap)

if __name__ == '__main__':
    parser = ArgumentParser("Reflector Agent")
    parser.add_argument('-u', '--username', required = True, type=str, help = "Username of the account to run the agent on")
    parser.add_argument('-p', '--password', required = True, type=str, help = "Password of the account to run the agent on")

    args = parser.parse_args()

    agent = ReflectorAgent(args.username, args.password)
    agent.listen()
