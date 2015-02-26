import tempfile, mimetypes, datetime, subprocess, re, math, os
from PIL import Image
from constants import MEDIA_TYPE_IMAGE, MEDIA_TYPE_VIDEO, MEDIA_TYPE_VIDEO_WITHOUT_AUDIO, SNAP_IMAGE_DIMENSIONS

def file_extension_for_type(media_type):
    if media_type is MEDIA_TYPE_IMAGE:
        return ".jpg"
    else:
        return ".mp4"

def create_temporary_file(suffix):
    return tempfile.NamedTemporaryFile(suffix=suffix, delete=False)

def save_snap(snap,dir_name):
    now = datetime.datetime.now()
    before_folder = os.getcwd()
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    os.chdir(dir_name)
    filename = '%s-%s-%s_%s:%s:%s_%s%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second, snap.sender, snap.file.name[-4:])
    with open(filename, 'wb') as f:
        data = snap.file.file.read(8192)
        while data:
            f.write(data)
            data = snap.file.file.read(8192)
    os.chdir(before_folder)

def is_video_file(path):
    return mimetypes.guess_type(path)[0].startswith("video")

def is_image_file(path):
    return mimetypes.guess_type(path)[0].startswith("image")

def guess_type(path):
    if is_video_file(path): return MEDIA_TYPE_VIDEO
    if is_image_file(path): return MEDIA_TYPE_IMAGE
    return MEDIA_TYPE_UNKNOWN

def resize_image(im, output_path):
    im.thumbnail(SNAP_IMAGE_DIMENSIONS, Image.ANTIALIAS)
    im.save(output_path, quality = 100)

def duration_string_to_timedelta(s):
    [hours, minutes, seconds] = map(int, s.split(':'))
    seconds = seconds + minutes * 60 + hours * 3600
    return datetime.timedelta(seconds=seconds)

def get_video_duration(path):
    result = subprocess.Popen(["ffprobe", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    matches = [x for x in result.stdout.readlines() if "Duration" in x]
    duration_string = re.findall(r'Duration: ([0-9:]*)', matches[0])[0]
    return math.ceil(duration_string_to_timedelta(duration_string).seconds)
