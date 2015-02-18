import time, urllib2, textwrap, re, HTMLParser, tempfile
from PIL import Image, ImageDraw, ImageFont
from argparse import ArgumentParser
from snapchat_bots import SnapchatBot, Snap
from snapchat_bots.utils import resize_image

h = HTMLParser.HTMLParser()


def get_article_info(url):
    content = urllib2.urlopen(url).read()
    description = re.search("<meta name=\"Description\" content=\"([^\"]*)", content).group(1)
    img_src = re.search("<meta property=\"og:image\" content=\"([^\"]*)", content).group(1)
    img = download_image(img_src)
    return h.unescape(description), img


def download_image(src):
    tmp = tempfile.NamedTemporaryFile(suffix = ".jpg")
    tmp.write(urllib2.urlopen(src).read())
    img = Image.open(tmp.name)
    return img


def get_last_breaking_news_url():
    content = urllib2.urlopen("https://twitter.com/BBCBreaking").read()
    try:
        return re.search('http://bbc.in[^<\"]*', content).group(0)
    except:
        pass


def create_breaking_news_image_from_info(info):
    title, header_img = info
    para = textwrap.wrap(title, width=30)
    im = Image.new('RGB', (290, 600), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('resources/Arial.ttf', 19)

    current_h, pad = 100, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((290 - w) / 2, current_h), line, font=font)
        current_h += h + pad

    current_h += 40

    im.paste(header_img, (0, current_h))

    return im


class ReporterBot(SnapchatBot):
    def initialize(self):
        self.last_tweet_url = None

    def on_friend_add(self, friend):
        self.add_friend(friend)

    def on_friend_delete(self, friend):
        self.delete_friend(friend)

    def run(self):
        while True:
            self.log("Checking news...")

            last_tweet_url = get_last_breaking_news_url()

            if self.last_tweet_url is None:
                self.last_tweet_url = last_tweet_url

            elif self.last_tweet_url != last_tweet_url:
                info = get_article_info(last_tweet_url)
                self.log("Found breaking news: %s" % info[0])
                img = create_breaking_news_image_from_info(info)
                snap = Snap.from_image(img, duration = 10)
                self.send_snap(self.get_friends(), snap)
                self.last_tweet_url = last_tweet_url

            else:
                self.log("No breaking news found")

            time.sleep(60)

if __name__ == '__main__':
    parser = ArgumentParser("Reporter Bot")
    parser.add_argument('-u', '--username', required = True, type=str, help = "Username of the account to run the bot on")
    parser.add_argument('-p', '--password', required = True, type=str, help = "Password of the account to run the bot on")

    args = parser.parse_args()

    bot = ReporterBot(args.username, args.password)
    bot.run()
