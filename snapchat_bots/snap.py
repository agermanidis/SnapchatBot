import subprocess, uuid, os
from PIL import Image
from StringIO import StringIO

from utils import guess_type, create_temporary_file, get_video_duration, resize_image, file_extension_for_type, default_filename_for_snap, cmd_exists, extract_zip_components
from constants import MEDIA_TYPE_IMAGE, MEDIA_TYPE_VIDEO, MEDIA_TYPE_VIDEO_WITHOUT_AUDIO, DEFAULT_DURATION, SNAP_IMAGE_DIMENSIONS
from exceptions import UnknownMediaType, CannotOpenFile

class Snap(object):
    @staticmethod
    def from_file(path, duration = None):
        media_type = guess_type(path)

        if media_type is MEDIA_TYPE_VIDEO or media_type is MEDIA_TYPE_VIDEO_WITHOUT_AUDIO:
            if duration is None: duration = get_video_duration(path)
            tmp = create_temporary_file(".snap.mp4")
            output_path = tmp.name
            subprocess.Popen(["ffmpeg", "-y", "-i", path, output_path]).wait()

        elif media_type is MEDIA_TYPE_IMAGE:
            image = Image.open(path)
            tmp = create_temporary_file(".jpg")
            output_path = tmp.name
            resize_image(image, output_path)
            if not duration:
                duration = DEFAULT_DURATION

        else:
            raise UnknownMediaType("Could not determine media type of the file")

        return Snap(path=output_path, media_type=media_type, duration=duration)

    @staticmethod
    def from_image(img, duration=DEFAULT_DURATION):
        f = create_temporary_file(".jpg")
        resize_image(img, f.name)
        return Snap(path=f.name, media_type=MEDIA_TYPE_IMAGE, duration=duration)

    def is_image(self):
        return media_type is MEDIA_TYPE_IMAGE

    def is_video(self):
        return media_type is MEDIA_TYPE_VIDEO or media_type is MEDIA_TYPE_VIDEO_WITHOUT_AUDIO

    def open(self):
        if not cmd_exists("open"):
            raise CannotOpenFile("Cannot open file")

        subprocess.Popen(["open", self.file.name])
 
    def save(self, output_filename = None, dir_name = "."):
        if output_filename is None:
            output_filename = default_filename_for_snap(self)
        
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(os.path.join(dir_name, output_filename), 'wb') as f:
            data = self.file.file.read(8192)
            while data:
                f.write(data)
                data = self.file.file.read(8192)

    def __init__(self, **opts):
        self.uploaded = False
        self.duration = opts['duration']
        self.media_type = opts['media_type']

        if opts.get("is_story", False):
            self.story_id = opts['snap_id']

        if 'sender' in opts:
            self.sender = opts['sender']
            self.snap_id = opts['snap_id']
            self.from_me = False

        else:
            self.snap_id = uuid.uuid4().hex
            self.from_me = True

        if 'data' in opts:
            data = opts['data']

            if data[0:2] == 'PK':
                video_filename, _ = extract_zip_components(data)
                self.file = open(video_filename, 'rb+')

            else:
                suffix = file_extension_for_type(opts['media_type'])
                self.file = create_temporary_file(suffix)

            if self.media_type is MEDIA_TYPE_VIDEO or self.media_type is MEDIA_TYPE_VIDEO_WITHOUT_AUDIO:
                self.file.write(data)
                self.file.flush()

            else:
                image = Image.open(StringIO(data))
                resize_image(image, self.file.name)

        else:
            path = opts['path']
            self.file = open(path)
