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
    try:
        cleaned = raw_text.split('\"')
        if len(cleaned) <= 1:
            cleaned = raw_text.replace("\n\n", "")
        else:
            cleaned = cleaned[1]

        sub_list = cleaned.split("\n\n")
        if "Sure!" in sub_list[0] or "Here's a" in sub_list[0]:
            cleaned = "\n\n".join(sub_list[1:])
        else:
            cleaned = "\n\n".join(sub_list)

        cleaned = cleaned.replace("\"", "")
        cleaned = cleaned.replace("Example:", "")
        cleaned = cleaned.replace("Here's a possible tweet:", "")
        cleaned = cleaned.replace("Tweet:", "")
        cleaned = cleaned.replace(" Clarifai's"," @clarifai's")
        cleaned = cleaned.replace(" Clarifai "," @clarifai ")
        cleaned = cleaned.replace("#Clarifai's","@clarifai's")
        cleaned = cleaned.replace("#Clarifai", "@clarifai")
        cleaned = cleaned.replace('Clarifai!', '@clarifai!')
    except Exception:
        raise Exception("Raw output: %s, cleaned:%s" % (raw_text, str(cleaned)))
    return cleaned

def build_tweet_url(tweet_id:str, twitter_user_id:str = TWITTER_USER_ID) -> str:
    return "https://twitter.com/%s/status/%s" %(twitter_user_id, tweet_id)


def post_tweet(tweet: str) -> str:
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    response = client.create_tweet(
        text=tweet
    )
    return response.data['id']


def main():
    prompter = ClarifaiPrompter()

    while True:
        output = prompter.predict()
        tweet = clean_llm_output(output)
        if len(tweet) < 280 and "https" in tweet:
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
