import time, urllib2, textwrap, re, HTMLParser
from PIL import Image, ImageDraw, ImageFont
from argparse import ArgumentParser
from snapchat_agents import SnapchatAgent, Snap
from snapchat_agents.utils import resize_image

h = HTMLParser.HTMLParser()

def get_article_info(url):
    resp = requests.get(url)
    description = re.search("<meta name=\"Description\" content=\"([^\"]*)", resp.content).group(1)
    img_src = re.search("<meta property=\"og:image\" content=\"([^\"]*)", resp.content).group(1)
    return (h.unescape(description), img_src)

def download_image(src):
    tmp = tempfile.NamedTemporaryFile(suffix = ".jpg")
    tmp.write(urllib2.urlopen(src).read())
    img = Image.open(tmp.name)
    return img

def get_last_breaking_news_url():
    resp = requests.get("https://twitter.com/BBCBreaking")
    try:
        return re.search('http://bbc.in[^<\"]*', resp.content).group(0)
    except:
        pass

def create_breaking_news_image_from_article(title, img_src):
    para = textwrap.wrap(text, width=15)
    im = Image.new('RGB', (290, 600), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('resources/Arial.ttf', 25)

    current_h, pad = 100, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((290 - w) / 2, current_h), line, font=font)
        current_h += h + pad

    tmp = tempfile.NamedTemporaryFile(suffix = ".jpg")
    im.save(tmp.name)
    return tmp.name

class ReporterAgent(SnapchatAgent):
    def initialize(self):
        self.last_tweet_id = None

    def on_friend_add(self, friend):
        self.add_friend(friend)

    def on_friend_delete(self, friend):
        self.delete_friend(friend)

    def run(self):
        while True:
            # ...

            time.sleep(60)


if __name__ == '__main__':
    parser = ArgumentParser("Reporter Agent")
    parser.add_argument('-u', '--username', required = True, type=str, help = "Username of the account to run the agent on")
    parser.add_argument('-p', '--password', required = True, type=str, help = "Password of the account to run the agent on")

    args = parser.parse_args()

    agent = ReporterAgent(args.username, args.password)
    agent.run()
