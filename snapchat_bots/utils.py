import tempfile, mimetypes, datetime, subprocess, re, math, os
from PIL import Image
from constants import MEDIA_TYPE_IMAGE, MEDIA_TYPE_VIDEO, MEDIA_TYPE_VIDEO_WITHOUT_AUDIO, SNAP_IMAGE_DIMENSIONS
from zipfile import ZipFile

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def file_extension_for_type(media_type):
    if media_type is MEDIA_TYPE_IMAGE:
        return ".jpg"
    else:
        return ".mp4"

def create_temporary_file(suffix):
    return tempfile.NamedTemporaryFile(suffix=suffix, delete=False)

def default_filename_for_snap(snap):
    now = datetime.datetime.now()
    filename = '%s-%s-%s_%s-%s-%s_%s%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second, snap.sender, snap.file.name[-4:])
    return filename 
    
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

def extract_zip_components(data):
    tmp = create_temporary_file(".zip")
    tmp.write(data)
    tmp.flush()
    zipped_snap = ZipFile(tmp.name)
    unzip_dir = os.path.join(tmp.name.split(".")[0])
    os.mkdir(unzip_dir)
    zipped_snap.extractall(unzip_dir)
    filenames = os.listdir(unzip_dir)
    for filename in filenames:
        if filename.startswith("media"):
            old_video_path = os.path.join(unzip_dir, filename)
            new_video_path = os.path.join(unzip_dir, "video.mp4")
            os.rename(old_video_path, new_video_path)

        elif filename.startswith("overlay"):
            overlay_component = os.path.join(unzip_dir, filename)

    return new_video_path, overlay_component

def duration_string_to_timedelta(s):
    [hours, minutes, seconds] = map(int, s.split(':'))
    seconds = seconds + minutes * 60 + hours * 3600
    return datetime.timedelta(seconds=seconds)

def get_video_duration(path):
    result = subprocess.Popen(["ffprobe", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    matches = [x for x in result.stdout.readlines() if "Duration" in x]
    duration_string = re.findall(r'Duration: ([0-9:]*)', matches[0])[0]
    return math.ceil(duration_string_to_timedelta(duration_string).seconds)

