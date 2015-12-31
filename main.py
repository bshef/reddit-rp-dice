#!/usr/bin/python

import praw
import OAuth2Util
from pprint import pprint
import time
from commandParser import Parser
import config

class Bot:
    # Class fields
    subreddit_name = ''
    is_logged_in = False
    need_to_exit = False
    reddit = None
    oauth = None
    processed_submissions = []
    processed_comments = []

    def __init__(self, subreddit_name):
        self.reddit = praw.Reddit(user_agent=config.user_agent)
        self.subreddit_name = subreddit_name
        self.login()

    # Log in as a Reddit client
    def login(self):
        global oauth, reddit
        if config.use_oauth:
            print 'Using OAuth2 to log in to Reddit ... '
            self.oauth = OAuth2Util.OAuth2Util(reddit)
            self.oauth.refresh(force=True)
        else:
            print 'Using username & password to log in to Reddit ... '
            self.reddit.login(username=config.username, password=config.password, disable_warning=True)
        print ' ... Connected'

    # Parse a comment's body text for a command
    def parseCommentForCommand(self, comment):
        body = comment.body
        result = Parser.parse_for_command(body)
        if result is not None:
            msg = '>/u/{0} {1}  \n  \nResult: **{2}**'.format(comment.author, body, result)
            reply = comment.reply(msg)
            print 'Replied to comment {0} by {1} with reply{2}:\n{3}\n'.format(comment.id, comment.author, reply.id, reply.body)

    # Scan all comments (flattened) under a submission
    def scanComments(self, submission):
        print 'Submission {0} by {1}: {2}'.format(submission.id, submission.author, submission.title)
        comments = praw.helpers.flatten_tree(submission.comments)
        print ' ... found {0} comments.'.format(len(comments))
        for comment in comments:
            if comment.id not in self.processed_comments and comment.author != config.username:
                self.parseCommentForCommand(comment)
                self.processed_comments.append(comment.id)

    # Scan all submissions within a subreddit
    def scanSubredditSubmissions(self, subreddit):
        if(subreddit is not None):
            try:
                new_submissions = subreddit.get_new()
                for submission in new_submissions:
                    if submission.id not in self.processed_submissions:
                        self.scanComments(submission)
                        self.processed_submissions.append(submission.id)
            except Exception as e :
                pprint(e)
        else:
            print 'No subreddit found'

    # The main logic loop of the Bot class
    def work(self):
        attempt = 1
        max_attempts = 30
        while not self.need_to_exit:
            subreddit = self.reddit.get_subreddit(self.subreddit_name)
            if subreddit:
                self.scanSubredditSubmissions(subreddit)
                print 'Sleeping for {0} seconds ... '.format(config.sleep_seconds)
                time.sleep(config.sleep_seconds)
            else:
                if attempt < max_attempts:
                    attempt += 1
                    print 'Attempting to connect to subreddit {0} (try {1}/{2})... '.format(self.subreddit_name, attempt, max_attempts)
                    time.sleep(1)
                else:
                    self.need_to_exit = True
                    print 'Exiting ... '
        print 'Done.'

# Main logic
def main():
    bot = Bot('redditrpdice')
    bot.work()

# Script main entry point
if __name__ == '__main__':
    main()



