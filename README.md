# SnapchatBot: Building bots that live on Snapchat

Introducing SnapchatBot, an easy way to program Snapchat accounts to do anything you want.
SnapchatBot can be used to easily create image-based notification services, chatbots, search interfaces,
and any kind of intelligent agent that uses picture messages as its interaction mode.

Uses the Snapchat's unofficial API as disclosed by [GibSec](http://gibsonsec.org/snapchat/fulldisclosure/).

## Bots Included

#### The Reflector
*(add TheReflector on Snapchat; source at examples/reflector.py)*

Sends back everything you send it.

#### The Storifier
*(add TheStorifier on Snapchat; source at examples/storifier.py)*

Takes all the snaps sent to it and adds them to its story. It can be used to collect responses
from multiple people around a single theme, much like a Twitter hashtag.

#### The Auto-Welcomer
*(add TheAutoWelcomer on Snapchat; source at examples/autowelcomer.py)*

Sends you an auto-welcome message when you add it to your friends.

#### The Reporter
*(add TheReporter on Snapchat; source at examples/reporter.py)*

Sends you a snap when breaking news happen. Follows the [BBC Breaking News twitter account](https://twitter.com/bbcbreaking).

#### The Googler
*(add TheResearcher on Snapchat; source at examples/googler.py)*

When sent an image, sends back the most similar image to that picture on the web. Uses Google Image Search.

#### The GIF Maniac
*(add TheGIFManiac on Snapchat; source at examples/gifmaniac.py)*

Posts popular GIFs taken from the [Giphy](http://giphy.com) home page to its story.

#### The Connector
*(add TheConnector on Snapchat; source at examples/connector.py)*

When you add the Connector to your friends, it links you with a stranger who's also added it. Every snap sent to the Connector will then arrive at the stranger's inbox, and all snaps sent from the stranger to the Connector will come to you. It's like ChatRoulette on Snapchat.

## Installation

    $ python setup.py install

You also need to have [ffmpeg](https://www.ffmpeg.org/) and [ImageMagick](http://www.imagemagick.org/) installed.

## How to build your own bots

`SnapchatBot` currently supports the following methods:

* `SnapchatBot#send_snap(recipients, snap)` -- sends snap `snap` to the list of usernames `recipients`
* `SnapchatBot#add_friend(username)` -- adds user with username `username` to the bot's friends
* `SnapchatBot#delete_friend(username)` -- deletes user with username `username` from the bot's friends
* `SnapchatBot#block(username)` -- blocks user with username `username`
* `SnapchatBot#get_snaps(mark_viewed = True)` -- gets snaps in the bot's inbox that haven't been viewed yet (use `mark_viewed = False` as a keyword argument if you don't want the bot to mark every snap received as viewed)
* `SnapchatBot#mark_viewed(snap)` -- marks `snap` as viewed
* `SnapchatBot#get_friends()` -- gets the bot's friends
* `SnapchatBot#get_added_me()` -- gets all users that have added the bot to their friends
* `SnapchatBot#listen()` -- listens to events (and triggers `on_snap`, `on_friend_add`, or `on_friend_delete`, if they are defined)

To create a snap to send with your bot, either use `Snap.from_file(path_to_file)` with a path
to an image or a video, or create an image with PIL and then use `Snap.from_image(img)`.

To define behaviors for your bot in response to various events (right now only
incoming snaps, friend additions, and friend deletions are supported) subclass `SnapchatBot`
and define any subset of the following methods:

* `initialize` -- run when the bot is created
* `on_snap` -- run when the bot bot receives a snap
* `on_friend_add` -- run when a Snapchat user adds the bot
* `on_friend_delete` -- run when a Snapchat user deletes the bot

To begin listening to events, use the `SnapchatBot#listen` method.

For example, here is the code for the `ReflectorBot`, which simply responds to a snap by sending it
back to the user who sent it:

```python
class ReflectorBot(SnapchatBot):
  # when receiving a snap, sends the same snap back to the sender
  def on_snap(self, sender, snap):
    self.send_snap([sender], snap)

  # when someone adds the bot, the bot adds them back
  def on_friend_add(self, friend):
    self.add_friend(self, friend)

  # when someone deletes the bot, the bot deletes them too
  def on_friend_delete(self, friend):
    self.delete_friend(self, friend)
```

Then to run the bot:

```python
bot = ReflectorBot(<account username>, <account password>)
bot.listen()
```
