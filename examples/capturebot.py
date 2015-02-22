import time
from argparse import ArgumentParser

from snapchat_bots import SnapchatBot


class CaptureBot(SnapchatBot):
    def on_snap(self, sender, snap):
        self.send_snap([sender], snap)
    
    def listen(self, timeout=15):
        while True:
            self.log("Querying for new snaps...")
            snaps = self.get_snaps(capture_snaps=True)
            for snap in snaps:
                self.on_snap(snap.sender, snap)

            time.sleep(timeout)

if __name__ == '__main__':
    parser = ArgumentParser("Capture Bot")
    parser.add_argument('-u', '--username', required=True, type=str, help="Username of the account to run the bot on")
    parser.add_argument('-p', '--password', required=True, type=str, help="Password of the account to run the bot on")

    args = parser.parse_args()

    bot = CaptureBot(args.username, args.password)
    bot.listen(timeout=60)
