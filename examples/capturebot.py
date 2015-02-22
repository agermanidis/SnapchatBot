from argparse import ArgumentParser
from snapchat_bots import SnapchatBot
from snapchat_bots.utils import save_snap

class CaptureBot(SnapchatBot):
    def on_snap(self, sender, snap):
        save_snap(snap)
        self.send_snap([sender], snap)
    

if __name__ == '__main__':
    parser = ArgumentParser("Capture Bot")
    parser.add_argument('-u', '--username', required=True, type=str, help="Username of the account to run the bot on")
    parser.add_argument('-p', '--password', required=True, type=str, help="Password of the account to run the bot on")

    args = parser.parse_args()

    bot = CaptureBot(args.username, args.password)
    bot.listen(timeout=60)