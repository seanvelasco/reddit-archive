import praw
import re
import pathlib
import urllib.parse
import ffmpeg
import json

# Target subreddit
target_subreddit = ""

# Specify if 'best,' 'hot,' 'new,' 'rising,' 'controversial,' 'top,' 'gilded,' 'wiki'
target_type = "top"

# Specify limit
number = "100"

# Specify destination of scraped data
path = str(pathlib.Path(__file__).resolve().parent) + '//output//'

    
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)
def scrape():

    entries = {}

    for submission in reddit.subreddit(target_subreddit).top(limit=50000):
        video = re.search("^http(s)?://v\.redd\.it/\w+$", submission.url)
        image = re.search("^http(s)?://i\.redd\.it/\w+\.(png|gif|jpg|jpeg)$", submission.url)
        filetype = re.search("(png|gif|jpg|jpeg)", submission.url)
        if video:
            entries[submission.id] = {
                "title" : submission.title,
                "url" : submission.url,
                "filename": submission.id + '.mp4'
            }
            get_video(submission)
        if image:
            entries[submission.id] = {
                "title" : submission.title,
                "url" : submission.url,
                "filename": submission.id + '.' + filetype.group()
            }
            get_image(submission, filetype)
        else:
            continue

    with open('entries.json', 'w') as outfile:
        json.dump(entries, outfile, indent=4)        

def get_video(submission):
    if submission.secure_media['reddit_video']['dash_url']:
        try:
            stream = ffmpeg.input(submission.secure_media['reddit_video']['dash_url'])
            stream = ffmpeg.output(stream, path + submission.id + ".mp4")
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as error:
                print('stdout:', error.stdout.decode('utf8'))
                print('stderr:', error.stderr.decode('utf8'))
                pass

def get_image(submission, filetype):
    urllib.request.urlretrieve(submission.url, path + submission.id + "." + filetype.group() )


scrape()