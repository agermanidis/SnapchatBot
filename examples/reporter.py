import time, urllib2
from argparse import ArgumentParser
from snapchat_agents import SnapchatAgent, Snap

def retrieve_breaking_news():
    # should return {text: str, image: url}
    
    pass

class ReporterAgent(SnapchatAgent):
    def initialize(self):
        self.last_tweet_id = None

    def create_snap_from_tweet(self, text):
        pass

    def get_last_news(self):
        # get twitter timeline
        # get last tweet
        # compare with existing tweet
        # if new tweet then
        pass

    def run(self):
        while True:
            pass

if __name__ == '__main__':
    parser = ArgumentParser("Reporter Agent")
    parser.add_argument('-u', '--username', required = True, type=str, help = "Username of the account to run the agent on")
    parser.add_argument('-p', '--password', required = True, type=str, help = "Password of the account to run the agent on")

    args = parser.parse_args()

    agent = ReporterAgent(args.username, args.password)
    agent.run()
