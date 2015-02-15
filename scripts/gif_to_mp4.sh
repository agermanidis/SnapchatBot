# taken from https://gist.github.com/avioli/9622038 with adjustments

# requires imagemagick and ffmpeg (tested with latest versions)
# make sure you set an INFILE variable first

# get GIF info
video=$(ffmpeg -y -i "$1" 2>&1 /dev/null | grep "Video:");

# get GIF Frames per second
fps=$(echo "$video" | sed -n "s/.* \([0-9.]*\) fps.*/\1/p");

# a convinience variable so we can easily set FPS on the video
fps1000=$(echo "scale=0;$fps*100000/100" | bc);

mkdir temp_dir;

# extract the frames in sequental PNGs
convert -coalesce "$1" temp_dir/temp%d.png;

# sequence the PNGs into an MP4 container (libx264 encoded by default)
ffmpeg -y -f image2 -r "$fps1000/1000" -i temp_dir/temp%d.png -v:b 1500 -an -vf scale="290:600" "$2"

# remove the temporary PNGs
rm -rf temp_dir;

# notes:
#   fps detection is not thoroughly tested, thus not reliable; one could read the GIF and calculate each frame's delay (would allow variable frame rate GIF detection as well)
#   "convert -coalesce" makes disposable GIFs to export as full frames
#   "ffmpeg ... -vf scale=..." ensures MP4 output dimensions is divisable by 2 (a rather unoptimized calculation)
