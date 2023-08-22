import os
import tweepy

from constants import TWITTER_USER_ID
from llm import ClarifaiPrompter
from upload import ClarifaiUploader

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


def clean_llm_output(raw_text: str) -> str:
    cleaned = raw_text.split('\n\n')[1]
    cleaned = cleaned.replace("\"", "")
    cleaned = cleaned.replace("Example: ", "")
    return cleaned

def build_tweet_url(tweet_id:str) -> str:
    return "https://twitter.com/%s/status/%s" %(TWITTER_USER_ID, tweet_id)

def main():
    prompter = ClarifaiPrompter()

    while True:
        output = prompter.predict()
        tweet = clean_llm_output(output)
        if len(tweet) < 280:
            break

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    response = client.create_tweet(
        text=tweet
    )
    tweet_id = response.data['id']
    print(f"Tweet ID: {tweet_id}")

    tweet_url = build_tweet_url(tweet_id)
    image_path = f"{tweet_id}.png"
    
    ## https://github.com/xacnio/tweetcapture/blob/main/tweetcapture/examples/tweet_screenshot.py
    from tweetcapture import TweetCapture
    import asyncio
    tweet = TweetCapture()
    asyncio.run(tweet.screenshot(tweet_url, image_path, mode=3, night_mode=0))

    ClarifaiUploader().upload(image_file_location=image_path)


if __name__ == "__main__":
    main()