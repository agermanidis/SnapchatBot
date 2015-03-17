import logging, time, uuid, requests, base64
from pysnap import Snapchat
from pysnap.utils import make_request_token, timestamp
from snap import Snap
from constants import DEFAULT_TIMEOUT, STATIC_TOKEN, BASE_URL

FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.level = logging.DEBUG

class SnapchatBot(object):
    def __init__(self, username, password, **kwargs):
        self.bot_id = uuid.uuid4().hex[0:4]

        self.auth_token = STATIC_TOKEN

        self.username = username
        self.password = password

        r = self._make_request("/loq/login", {
            'username': self.username,
            'password': self.password
        })

        result = r.json()
        self.auth_token = result['updates_response']['auth_token']

        self.client = Snapchat()
        self.client.username = username
        self.client.auth_token = self.auth_token

        self.current_friends = self.get_friends()
        self.added_me = self.get_added_me()

        if hasattr(self, "initialize"):
            self.initialize(**kwargs)

    def log(self, message, level=logging.DEBUG):
        logger.log(level, "[%s-%s] %s" % (self.__class__.__name__, self.bot_id, message))

    @staticmethod
    def process_snap(snap_obj, data, is_story = False):
        media_type = snap_obj["media_type"]
        sender = snap_obj["sender"]
        snap_id = snap_obj['id']
        duration = snap_obj['time']
        snap = Snap(data=data,
                    snap_id=snap_id,
                    media_type=media_type,
                    duration=duration,
                    sender=sender,
                    is_story=is_story)
        return snap

    def mark_viewed(self, snap):
        self.client.mark_viewed(snap.snap_id)

    def listen(self, timeout=DEFAULT_TIMEOUT):
        while True:
            self.log("Querying for new snaps...")
            snaps = self.get_snaps()

            if hasattr(self, "on_snap"):
                for snap in snaps:
                    self.on_snap(snap.sender, snap)

            added_me = self.get_added_me()

            newly_added = set(added_me).difference(self.added_me)
            newly_deleted = set(self.added_me).difference(added_me)

            self.added_me = added_me

            if hasattr(self, "on_friend_add"):
                for friend in newly_added:
                    self.log("User %s added me" % friend)
                    self.on_friend_add(friend)

            if hasattr(self, "on_friend_delete"):
                for friend in newly_deleted:
                    self.log("User %s deleted me" % friend)
                    self.on_friend_delete(friend)

            time.sleep(timeout)

    def get_friends(self):
        return map(lambda fr: fr['name'], self.client.get_friends())

    def get_added_me(self):
        updates = self.client.get_updates()
        return map(lambda fr: fr['name'], updates["added_friends"])

    def send_snap(self, recipients, snap):
        media_id = self._upload_snap(snap)

        if type(recipients) is not list:
            recipients = [recipients]

        recipients_str = ','.join(recipients)

        self.log("Sending snap %s to %s" % (snap.snap_id, recipients_str))

        self.client.send(media_id, recipients_str, snap.duration)

    def post_story(self, snap):
        media_id = self._upload_snap(snap)
        response = self.client.send_to_story(media_id, snap.duration, snap.media_type)

        try:
            snap.story_id = response['json']['story']['id']
        except:
            pass

    def delete_story(self, snap):
        print snap.story_id 
        if snap.story_id is None:
            return

        self.client._request('delete_story', {
            'username': self.username,
            'story_id': snap.story_id
        })

    def add_friend(self, username):
        self.client.add_friend(username)

    def delete_friend(self, username):
        self.client.delete_friend(username)

    def block(self, username):
        self.client.block(username)

    def process_snaps(self, snaps, mark_viewed = True):
        ret = []

        for snap_obj in snaps:
            if snap_obj['status'] == 2:
                continue

            data = self.client.get_blob(snap_obj["id"])

            if data is None:
                continue

            snap = self.process_snap(snap_obj, data)

            if mark_viewed:
                self.mark_viewed(snap)

            ret.append(snap)

        return ret

    def process_stories(self, stories):
        ret = []
        for snap_obj in stories:
            media_key = base64.b64decode(snap_obj['media_key'])
            media_iv = base64.b64decode(snap_obj['media_iv'])
            data = self.client.get_story_blob(snap_obj['media_id'],
                                              media_key,
                                              media_iv)
            if data is None:
                continue
            snap_obj['sender'] = self.username
            snap = self.process_snap(snap_obj, data, is_story = True)
            ret.append(snap)
        return ret

    def get_snaps(self, mark_viewed=True):
        snaps = self.client.get_snaps()
        return self.process_snaps(snaps)                

    def get_my_stories(self):
        response = self.client._request('stories', {
            'username': self.username
        })
        stories = map(lambda s: s['story'], response.json()['my_stories'])
        return self.process_stories(stories)

    def get_friend_stories(self):
        response = self.client._request('stories', {
            'username': self.username
        })
        ret = []
        stories_per_friend = map(lambda s: s['stories'], response.json()['friend_stories'])
        for stories_obj in stories_per_friend:
            stories = map(lambda so: so['story'], stories_obj)
            ret.extend(self.process_stories(stories))
        return ret

    def clear_stories(self):
        for story in self.get_my_stories():
            self.delete_story(story)

    def _upload_snap(self, snap):
        if not snap.uploaded:
            snap.media_id = self.client.upload(snap.file.name)
            snap.uploaded = True

        return snap.media_id

    def _make_request(self, path, data = None, method = 'POST', files = None):
        if data is None:
            data = {}

        headers = {
            'User-Agent': 'Snapchat/8.1.1 (iPhone5,1; iOS 8.1.3; gzip)',
            'Accept-Language': 'en-US;q=1, en;q=0.9',
            'Accept-Locale': 'en'
        }

        now = timestamp()

        if method == 'POST':
            data['timestamp'] = now
            data['req_token'] = make_request_token(self.auth_token, str(now))
            resp = requests.post(BASE_URL + path, data = data, files = files, headers = headers)
        else:
            resp = requests.get(BASE_URL + path, params = data, headers = headers)

        return resp
