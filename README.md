# SnapchatAgent: Building bots that live on Snapchat

Introducing SnapchatAgent, an easy way to program Snapchat accounts to do anything you want.
SnapchatAgent can be used to easily create image-based notification services, chatbots, search interfaces,
generally any kind of bot that uses picture messages as its interaction mode.

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

When you add the Connector to your friends, it links you with another user who's also added it. Every snap sent to the Connector will then arrive at the other person's inbox.

## Installation

    $ python setup.py install

You also need to have [ffmpeg](https://www.ffmpeg.org/) and [ImageMagick](http://www.imagemagick.org/) installed.

## How to build your own agents

`SnapchatAgent` currently supports the following methods:

* `SnapchatAgent#send_snap(recipients, snap)` -- sends snap `snap` to the list of usernames `recipients`
* `SnapchatAgent#add_friend(username)` -- adds user with username `username` to the agent's friends
* `SnapchatAgent#delete_friend(username)` -- deletes user with username `username` from the agent's friends
* `SnapchatAgent#block(username)` -- blocks user with username `username`
* `SnapchatAgent#get_snaps(mark_viewed = True)` -- gets snaps in the agent's inbox that haven't been viewed yet (use `mark_viewed = False` as a keyword argument if you don't want the agent to mark every snap received as viewed)
* `SnapchatAgent#mark_viewed(snap)` -- marks `snap` as viewed
* `SnapchatAgent#get_friends()` -- gets the agent's friends
* `SnapchatAgent#get_added_me()` -- gets all users that have added the agent to their friends
* `SnapchatAgent#listen()` -- listens to events (and triggers `on_snap`, `on_friend_add`, or `on_friend_delete`, if they are defined)

To create a snap to send with your agent, either use `Snap.from_file(path_to_file)` with a path
to an image or a video, or create an image with PIL and then use `Snap.from_image(img)`.

To define behaviors for your agent in response to various events (right now only
incoming snaps, friend additions, and friend deletions are supported) subclass `SnapchatAgent`
and define any subset of the following methods:

* `initialize` -- run when the agent is created
* `on_snap` -- run when the agent agent receives a snap
* `on_friend_add` -- run when a Snapchat user adds the agent
* `on_friend_delete` -- run when a Snapchat user deletes the agent

To begin listening to events, use the `SnapchatAgent#listen` method.

For example, here is the code for the `ReflectorAgent`, which simply responds to a snap by sending it
back to the user who sent it:

```python
class ReflectorAgent(SnapchatAgent):
  # when receiving a snap, sends the same snap back to the sender
  def on_snap(self, sender, snap):
    self.send_snap([sender], snap)

  # when someone adds the agent, the agent adds them back
  def on_friend_add(self, friend):
    self.add_friend(self, friend)

  # when someone deletes the agent, the agent deletes them too
  def on_friend_delete(self, friend):
    self.delete_friend(self, friend)
```

Then to run agent:

```python
agent = ReflectorAgent(<account username>, <account password>)
agent.listen()
```
