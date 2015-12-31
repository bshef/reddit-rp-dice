import praw
import OAuth2Util
from pprint import pprint
import time
from commandParser import Parser
import config


class Bot:
    # Class fields
    logged_in = False
    need_to_exit = False
    reddit = None
    oauth = None
    processed_submissions = []
    processed_comments = []

    def __init__(self):
        self.reddit = praw.Reddit(user_agent=config.user_agent)
        self.login()

    # Log in as a Reddit client
    def login(self):
        global oauth, reddit
        if config.use_oauth:
            print 'Using OAuth2 to log in to Reddit ... '
            self.oauth = OAuth2Util.OAuth2Util(reddit)
            self.oauth.refresh(force=True)
            while not self.logged_in:
                self.logged_in = self.reddit.is_oauth_session() and self.reddit.get_me() is not None
                time.sleep(1)
        else:
            print 'Using username & password to log in to Reddit ... '
            self.reddit.login(username=config.username, password=config.password, disable_warning=True)
            while not self.logged_in:
                self.logged_in = self.reddit.is_logged_in()
                time.sleep(1)
        print ' ... Connected'

    # Parse a comment's body text for a command
    @staticmethod
    def parse_comment_for_command(comment):
        body = comment.body
        result = Parser.parse_for_command(body)
        if result is not None:
            msg = '>/u/{0} {1}  \n  \nResult: **{2}**'.format(comment.author, body, result)
            reply = comment.reply(msg)
            print 'Replied to comment {0} by {1} with reply{2}:\n{3}\n'.format(
                comment.id, comment.author, reply.id, reply.body)

    # Scan all comments (flattened) under a submission
    def scan_comments(self, submission):
        print 'Submission {0} by {1}: {2}'.format(submission.id, submission.author, submission.title)
        comments = praw.helpers.flatten_tree(submission.comments)
        print ' ... found {0} comments.'.format(len(comments))
        for comment in comments:
            if comment.id not in self.processed_comments and comment.author != config.username:
                Bot.parse_comment_for_command(comment)
                self.processed_comments.append(comment.id)

    # Scan all submissions within a subreddit
    def scan_submissions(self, subreddit):
        if subreddit is not None:
            try:
                new_submissions = subreddit.get_new()
                for submission in new_submissions:
                    if submission.id not in self.processed_submissions:
                        self.scan_comments(submission)
                        self.processed_submissions.append(submission.id)
            except Exception as e:
                pprint(e)
        else:
            print 'No subreddit found'

    # The main logic loop of the Bot class
    def work(self):
        attempt = 1
        max_attempts = 30
        while not self.need_to_exit:
            subreddit = self.reddit.get_subreddit(config.subreddit_name)
            if subreddit:
                self.scan_submissions(subreddit)
                print 'Sleeping for {0} seconds ... '.format(config.sleep_seconds)
                time.sleep(config.sleep_seconds)
            else:
                if attempt < max_attempts:
                    attempt += 1
                    print 'Attempting to connect to subreddit {0} (try {1}/{2})... '.format(
                        config.subreddit_name, attempt, max_attempts)
                    time.sleep(1)
                else:
                    self.need_to_exit = True
                    print 'Exiting ... '
        print 'Done.'
