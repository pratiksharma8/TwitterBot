import tweepy
import time
print("This is my Twitter bot.")

CONSUMER_KEY = 'eBICX5kwenZb7pJsXBcBUIOSg'
CONSUMER_SECRET = '98SNBFeVbwZUUVJ3VzHwjVSpQM0FJitOqimZ0W8AqjS4ptU8Jc'
ACCESS_KEY = '1339459046-4OWBHtjvVr3tk8EvxkBBOWW1EybO7bVVMR2U53J'
ACCESS_SECRET = '8C6TZiFnlE8YFSkAD2reSZNMmpqW9xEv6vJhdjvYJSJwp'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('Retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#patbot' in mention.full_text.lower():
            print('Found #patbot!', flush=True)
            print('Responding back...', flush=True)
            api.update_status('Hello'+' '+'@'+mention.user.screen_name+' '+',I will get back to you!', mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)
