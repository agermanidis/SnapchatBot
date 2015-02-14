import time
from argparse import ArgumentParser
from snapchat_agents import SnapchatAgent

class GIFManiacAgent(SnapchatAgent):
    def run(self):
        while True:
            # grab gifs

            # create video snaps from gifs

            # for every video snap, add to story

            # sleep for an hour
            time.sleep(60 * 60)

if __name__ == '__main__':
    parser = ArgumentParser("GIF Maniac Agent")
    parser.add_argument('-u', '--username', required = True, type=str, help = "Username of the account to run the agent on")
    parser.add_argument('-p', '--password', required = True, type=str, help = "Password of the account to run the agent on")

    args = parser.parse_args()

    agent = GIFManiac(args.username, args.password)
    agent.run()
