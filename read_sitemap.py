import os
import tweepy
import requests
import pandas as pd
import random
import xmltodict

from constants import PROMPT_TEMPLATE, YEAR_ONWARDS, SITEMAP_URL, LASTMOD
from tweet import build_tweet_url
from llm import ClarifaiPrompter
from upload import ClarifaiUploader

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

def main():

    res = requests.get(SITEMAP_URL)
    raw = xmltodict.parse(res.text)
    data = [[r["loc"], r[LASTMOD]] for r in raw["urlset"]["url"]]
    df = pd.DataFrame(data, columns=["links", LASTMOD])
    df.sort_values(by='lastmod', ascending=False, inplace=True)

    df = df[df["links"].str.contains("blog")]
    df[LASTMOD] = pd.to_datetime(df[LASTMOD])
    df = df[df[LASTMOD]>f'{YEAR_ONWARDS}-01-01']

    chosen_url = random.choice(df['links'].tolist())
    print(f"{chosen_url=}")

    topic = chosen_url.split("/")[-1].replace('-',' ')
    print(f"{topic=}")

    prompt = PROMPT_TEMPLATE.safe_substitute(topic=topic, link=chosen_url)
    p = ClarifaiPrompter()

    while True:
        tweet = p.predict(prompt)
        if len(tweet) < 280 and "https" in tweet:
            break
    print(tweet)

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
