import time, tempfile, subprocess, re, datetime, mimetypes, logging, uuid
from pysnap import Snapchat, get_file_extension
from PIL import Image
from StringIO import StringIO

from utils import create_temporary_file, is_video_file, is_image_file, guess_type, resize_image, get_video_duration, MEDIA_TYPE_VIDEO, MEDIA_TYPE_IMAGE

FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.level = logging.DEBUG

DEFAULT_TIMEOUT = 3
DEFAULT_DURATION = 5

class Snap(object):
    @staticmethod
    def from_file(path, duration = None):
        media_type = guess_type(path)

        if media_type is MEDIA_TYPE_VIDEO:
            if duration is None: duration = get_video_duration(path)
            tmp = create_temporary_file(".mp4")
            output_path = tmp.name
            subprocess.Popen(["ffmpeg", "-i", path, out_path]).wait()

        elif media_type is MEDIA_TYPE_IMAGE:
            image = Image.open(path)
            tmp = create_temporary_file(".jpg")
            output_path = tmp.name
            resize_image(image, output_path)
            if duration is None: duration = DEFAULT_DURATION

        else:
            raise Exception, "Could not determine media type of the file"

        return Snap(path = output_path, media_type = media_type, duration = duration)

    @staticmethod
    def from_image(img, duration = DEFAULT_DURATION):
        f = create_temporary_file(".jpg")
        resize_image(img, f.name)
        return Snap(path = f.name, media_type = MEDIA_TYPE_IMAGE, duration = duration)

    def upload(self, agent):
        self.media_id = agent.client.upload(self.file.name)
        self.uploaded = True

    def __init__(self, **opts):
        self.uploaded = False
        self.duration = opts['duration']
        self.media_type = opts['media_type']

        if 'sender' in opts:
            self.sender = opts['sender']
            self.snap_id = opts['snap_id']
            self.from_me = False

        else:
            self.snap_id = uuid.uuid4().hex
            self.from_me = True

        if 'data' in opts:
            self.media_type = opts['media_type']

            suffix = "." + get_file_extension(opts['media_type'])

            self.file = create_temporary_file(suffix)

            if self.media_type is MEDIA_TYPE_VIDEO:
                self.file.write(opts['data'])
                self.file.flush()

            else:
                image = Image.open(StringIO(opts['data']))
                resize_image(image, self.file.name)

        else:
            path = opts['path']
            self.file = open(path)

class SnapchatAgent(object):
    def __init__(self, username, password, **kwargs):
        self.agent_id = uuid.uuid4().hex[0:4]

        self.username = username
        self.password = password

        self.client = Snapchat()
        self.client.login(username, password)

        self.current_friends = self.get_friends()
        self.added_me = self.get_added_me()

        if hasattr(self, "initialize"):
            self.initialize(**kwargs)

    def log(self, message, level = logging.DEBUG):
        logger.log(level, "[%s-%s] %s" % (self.__class__.__name__, self.agent_id, message))

    def process_snap(self, snap_obj, data):
        media_type = snap_obj["media_type"]
        sender = snap_obj["sender"]
        snap_id = snap_obj['id']
        duration = snap_obj['time']
        snap = Snap(data = data,
                    snap_id = snap_id,
                    media_type = media_type,
                    duration = duration,
                    sender = sender)
        return snap


    def mark_viewed(self, snap):
        self.client.mark_viewed(snap.snap_id)

    def listen(self, timeout = DEFAULT_TIMEOUT):
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
        self.log("Preparing to send snap %s" % snap.snap_id)

        if not snap.uploaded:
            self.log("Uploading snap %s" % snap.snap_id)
            snap.upload(self)

        if type(recipients) is not list:
            recipients = [recipients]

        recipients_str = ','.join(recipients)

        self.log("Sending snap %s to %s" % (snap.snap_id, recipients_str))

        self.client.send(snap.media_id, recipients_str)

    def post_story(self, snap):
        if not snap.uploaded:
            self.log("Uploading snap")
            snap.upload(self)

        self.log("Posting snap as story")
        self.client.send_to_story(snap.media_id, media_type = snap.media_type)

    def add_friend(self, username):
        self.client.add_friend(username)

    def delete_friend(self, username):
        self.client.delete_friend(username)

    def block(self, username):
        self.client.block(username)

    def get_snaps(self, mark_viewed = True):
        snaps = self.client.get_snaps()
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
