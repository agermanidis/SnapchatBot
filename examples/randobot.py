from argparse import ArgumentParser
from snapchat_bots import SnapchatBot, Snap
import random

class RandoBot(SnapchatBot):
    def initialize(self):
        self.connections = self.get_friends()
	#If your bot ever gets blocked, uncomment these lines.
	#Of course, make sure you have your old users backed up
	#to the users.txt file! So you must uncomment the first
	#three lines, while logged into the blocked bot, then
	#uncomment the rest to re-add all users from the old bot.
	#with open('users.txt', 'w') as file:
	#	for item in self.connections:
	#    		print>>file, item
	#f = open('users.txt', 'r')
	#for line in f:
	#	self.add_friend(line)
        #	print(line)
	print(self.connections)
		
    def connect(self,user):
        self.log("Added user: %s to the array!" % (user))
        self.connections.append(user)
		
    def on_friend_add(self,friend):
        self.add_friend(friend)
        self.connect(friend)

    def on_friend_delete(self,friend):
        self.delete_friend(friend)
        self.connections.remove(friend)
	
    def find_random_user(self,username):
	if len(self.connections) <= 1:
		return None
        newuser = random.choice(self.connections)
	while(newuser == username):
		newuser = random.choice(self.connections)
        return newuser

    def on_snap(self,sender,snap):
        connection = self.find_random_user(sender)
	if sender not in self.connections:
		self.send_snap([sender], Snap.from_file("../resources/rando_addme.png"))
    	if connection:
		self.send_snap([connection],snap)
		print("%s sent  snap to %s" % (sender,[connection]))
	else:
		self.send_snap([sender], Snap.from_file("../resources/rando_welcome.png"))
			
if __name__ == '__main__':
    parser = ArgumentParser("RandoBot Bot")
    parser.add_argument('-u', '--username', required=True, type=str, help="Username of the account to run the bot on")
    parser.add_argument('-p', '--password', required=True, type=str, help="Password of the account to run the bot on")

    args = parser.parse_args()

    bot = RandoBot(args.username, args.password)
    bot.listen(timeout=33)
