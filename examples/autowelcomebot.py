from argparse import ArgumentParser
from snapchat_bots import SnapchatBot, Snap


class AutoWelcomerBot(SnapchatBot):
    def on_friend_add(self, friend):
        self.send_snap(friend, Snap.from_file("resources/auto_welcome.png"))

    def on_friend_delete(self, friend):
        self.delete_friend(friend)

if __name__ == '__main__':
    parser = ArgumentParser("Auto-Welcomer Bot")
    parser.add_argument('-u', '--username', required=True, type=str, help="Username of the account to run the bot on")
    parser.add_argument('-p', '--password', required=True, type=str, help="Password of the account to run the bot on")

    args = parser.parse_args()

    bot = AutoWelcomerBot(args.username, args.password)
    bot.listen()