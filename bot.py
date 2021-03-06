
# A Reddit bot that posts the definition of a word when summoned in the comments.
# The word to be defined must be preceded by dftm+.
# Definitions come from Oxford Dictionaries (EN).
# Created by Luis F. Uceta
# License: MIT License

import praw
import requests
import time
from config import *
from getInfo import *

# Credentials, language and subreddits
app_id = ID
app_key = KEY
language = LANG
filename = 'commentID.txt'
submit_to = 'roomofbugs'

def bot_login():
    """Create an instance of Reddit class and return it."""
    print("Logging in...")

    reddit = praw.Reddit(client_id = client_id,
                          client_secret = client_secret,
                          password = password,
                          user_agent = user_agent, username = username)

    return reddit 

def run_bot(reddit):
    """Log in, loop through comments and apply a condition.""" 
    subreddit = reddit.subreddit(submit_to)
    comments = subreddit.stream.comments()
    
    for comment in comments:
        text = comment.body
        
        if 'dtfm+' in text.lower():
            whole_string = text.split('+')
            word_id = whole_string[1].strip()
            
            try:
                url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id
                r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
                definition = get_definition(json_data(r))
            except ValueError:
                print("Exception! Word no found!")
            except KeyError:
                print("Exception! No definition found!")
            else:
                comment_definition(comment, word_id, definition, filename)

        time.sleep(10)

    print("Waiting 2 minutes.\n")
    time.sleep(120)

def main():
    r = bot_login()
    while True:
        run_bot(r)

if __name__=='__main__':
    main()

