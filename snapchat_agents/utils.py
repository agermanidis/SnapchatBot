import tempfile, mimetypes, datetime, subprocess, re, math
from PIL import Image

SNAPCHAT_IMAGE_DIMENSIONS = (290, 600)

MEDIA_TYPE_UNKNOWN = -1
MEDIA_TYPE_IMAGE = 1
MEDIA_TYPE_VIDEO = 2
MEDIA_TYPE_VIDEO_NOAUDIO = 3

def create_temporary_file(suffix):
    return tempfile.NamedTemporaryFile(suffix = suffix, delete = False)

def is_video_file(path):
    return mimetypes.guess_type(path)[0].startswith("video")

def is_image_file(path):
    return mimetypes.guess_type(path)[0].startswith("image")

def guess_type(path):
    if is_video_file(path): return MEDIA_TYPE_VIDEO
    if is_image_file(path): return MEDIA_TYPE_IMAGE
    return MEDIA_TYPE_UNKNOWN

def resize_image(im, output_path):
    im.thumbnail(SNAPCHAT_IMAGE_DIMENSIONS, Image.ANTIALIAS)
    im.save(output_path)

def duration_string_to_timedelta(s):
    [hours, minutes, seconds] = map(int, s.split(':'))
    seconds = seconds + minutes * 60 + hours * 3600
    return datetime.timedelta(seconds = seconds)

def get_video_duration(path):
    result = subprocess.Popen(["ffprobe", path], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    matches = [x for x in result.stdout.readlines() if "Duration" in x]
    duration_string = re.findall(r'Duration: ([0-9:]*)', matches[0])[0]
    return math.ceil(duration_string_to_timedelta(duration_string).seconds)
