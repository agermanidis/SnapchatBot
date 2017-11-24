#!/usr/bin/python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from snapchat_bots import SnapchatBot, Snap
import os,time


class PostmanBot(SnapchatBot):

    def message(self, text, friend):
        os.system('convert -size 1080x1920 -background yellow -gravity Center -fill grey -pointsize 80 label:"'+str(text)+'" image.jpg')
        self.send_snap(friend, Snap.from_file('image.jpg'))
        os.system('rm image.jpg')
        self.log('Sent the message : ' + str(text) + ' ')


if __name__ == '__main__':
    parser = ArgumentParser('Postman Bot')
    parser.add_argument('-u', '--username', required=True, type=str,
                        help='Username of the account to run the bot on'
                        )
    parser.add_argument('-p', '--password', required=True, type=str,
                        help='Password of the account to run the bot on'
                        )
    parser.add_argument('-msg', required=False, type=str,
                        help='Messenge you want to send yourself.')
    parser.add_argument('-user', required=False, type=str, help='The user you want to the send the message to; needs to existe.')

    args = parser.parse_args()
    bot = PostmanBot(args.username, args.password)
    
    if args.msg and args.user:
        if args.user == "all" or args.user == "All":
            friends_list = bot.get_friends()
            for friends in friends_list:
                print(friends)
                time.sleep(0.1)
                bot.message(args.msg, friends)
            
        else:
            bot.message(args.msg,args.user)
    else:
        self.log("You need to provid a valid message and username.")
