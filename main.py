#!/usr/bin/python

import praw
import OAuth2Util
from pprint import pprint
import time
import commandParser
import config

# Globals
parser = None
reddit = None
oauth = None
processed_submissions = []
processed_comments = []

# Perform initialization of resources
def init():
    global parser, reddit
    parser = commandParser.Parser()
    reddit = praw.Reddit(user_agent=config.user_agent)
    login()


# Log in as a Reddit client
def login():
    global oauth, reddit
    if config.use_oauth:
        print 'Using OAuth2 to log in to Reddit ... '
        oauth = OAuth2Util.OAuth2Util(reddit)
        oauth.refresh(force=True)
    else:
        print 'Using username + password to log in to Reddit ... '
        reddit.login(username=config.username, password=config.password, disable_warning=True)
    print ' ... Connected'


# Parse a comment's body text for a command
def parseCommentForCommand(comment):
    body = comment.body
    result = parser.parseForCommand(body)
    print 'Parse comment for command result: {0}'.format(result)
    if result is not None:
        msg = '/u/{0} {1}  \nResult: {1}'.format(comment.author, body, result)
        reply = comment.reply(msg)
        print 'Replied to comment {0} by {1} with reply {2}: {3}'.format(comment.id, comment.author, reply.id, reply.body)
    else:
        print 'NO COMMAND FOUND in: \t\t {0}'.format(body)


# Scan all comments (flattened) under a submission
def scanComments(submission):
    print 'Submission {0} by {1}: {2}'.format(submission.id, submission.author, submission.title)
    comments = praw.helpers.flatten_tree(submission.comments)
    print ' ... found {0} comments.'.format(len(comments))
    for comment in comments:
        if comment.id not in processed_comments:
            parseCommentForCommand(comment)
            processed_comments.append(comment.id)


# Scan all submissions within a subreddit
def scanSubredditSubmissions(subreddit):
    if(subreddit is not None):
        try:
            new_submissions = subreddit.get_new(fetch=True)
            for submission in new_submissions:
                if submission.id not in processed_submissions:
                    scanComments(submission)
                    processed_submissions.append(submission.id)
        except Exception as e :
            pprint(e)
    else:
        print 'No subreddit found'
    print 'Sleeping ... '
    time.sleep(config.sleep_seconds)


# Main logic
def main():
    init()
    while True:
        scanSubredditSubmissions(reddit.get_subreddit('redditrpdice', fetch=True))


# Script main entry point
if __name__ == '__main__':
    main()



