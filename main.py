import praw
import re
import pathlib
import urllib.parse
from urllib.request import Request
from urllib.error import HTTPError
import ffmpeg
from ffmpeg import Error as FFmpegError

# Target subreddit

target_subreddit = ""

# Specify if 'best,' 'hot,' 'new,' 'rising,' 'controversial,' 'top,' 'gilded,' 'wiki'

target_type = ""

# Specify limit

limit = ""

# Specify destination of scraped data

path = 'D:\\reddit-regex-search\\output\\'

reddit = praw.Reddit(login)

def Scrape():
    for submission in reddit.subreddit(target_subreddit).top(limit):
        video = re.search("^http(s)?://v\.redd\.it/\w+$", submission.url)
        image = re.search("^http(s)?://i\.redd\.it/\w+\.(png|gif|jpg|jpeg)$", submission.url)
        filetype = re.search("(png|gif|jpg|jpeg)", submission.url)
        print(submission)
        print(submission.title)
        if video:
            print(video.group())
            if submission.secure_media['reddit_video']['dash_url']:
                try:
                    stream = ffmpeg.input(submission.secure_media['reddit_video']['dash_url'])
                    stream = ffmpeg.output(stream, path + submission.id + ".mp4")
                    ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
                except ffmpeg.Error as error:
                    print('stdout:', error.stdout.decode('utf8'))
                    print('stderr:', error.stderr.decode('utf8'))
                    raise error
        if image:
            print(image.group())
            urllib.request.urlretrieve(submission.url, path + submission.id + "." + filetype.group() )

Scrape()