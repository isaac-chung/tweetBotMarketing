import argparse
import logging
import os
import requests
import pandas as pd
import random
import xmltodict

from constants import (PROMPT_TEMPLATE, YEAR_ONWARDS, TWITTER_USER_ID,
                       SITEMAP_URL, LASTMOD, SYSTEM_PROMPTS)
from tweet import build_tweet_url, post_tweet
from llm import ClarifaiPrompter
from upload import ClarifaiUploader

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


def read_from_sitemap(url, blogs=True, year_onwards=YEAR_ONWARDS) -> str:
    """return a random URL from the sitemap after filtering for year of lastmod."""
    res = requests.get(url)
    raw = xmltodict.parse(res.text)
    data = [[r["loc"], r[LASTMOD]] for r in raw["urlset"]["url"]]
    df = pd.DataFrame(data, columns=["links", LASTMOD])
    df.sort_values(by='lastmod', ascending=False, inplace=True)

    if blogs:
        df = df[df["links"].str.contains("blog")]
    df[LASTMOD] = pd.to_datetime(df[LASTMOD])
    df = df[df[LASTMOD]>f'{year_onwards}-01-01']

    return random.choice(df['links'].tolist())


def main(args):
    sitemap_url = args.sitemap_url if args.sitemap_url else SITEMAP_URL
    chosen_url = read_from_sitemap(url=sitemap_url)
    logging.info(f"{chosen_url=}")

    topic = chosen_url.split("/")[-1].replace('-',' ')
    logging.info(f"{topic=}")

    system_prompt = random.choice(SYSTEM_PROMPTS)
    logging.info(f"{system_prompt=}")

    prompt = PROMPT_TEMPLATE.safe_substitute(system=system_prompt,
                                             topic=topic, link=chosen_url)
    p = ClarifaiPrompter()

    while True:
        tweet = p.predict(prompt)
        if len(tweet) < 280 and "https" in tweet:
            break
    logging.info(tweet)

    tweet_id = post_tweet(tweet)
    logging.info(f"Tweet ID: {tweet_id}")

    twitter_user_id = args.twitter_user_id if args.twitter_user_id else TWITTER_USER_ID
    tweet_url = build_tweet_url(tweet_id, twitter_user_id)

    if args.screenshot_and_upload:
        image_path = f"{tweet_id}.png"

        ## https://github.com/xacnio/tweetcapture/blob/main/tweetcapture/examples/tweet_screenshot.py
        from tweetcapture import TweetCapture
        import asyncio
        tc = TweetCapture()
        asyncio.run(tc.screenshot(tweet_url, image_path, mode=3, night_mode=0))

        ClarifaiUploader().upload(image_file_location=image_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      description='')
    parser.add_argument(
        '--screenshot_and_upload',
        help='Optional: Specify the url column name from csv file.',
        default=True,
        type=bool)
    parser.add_argument(
        '--sitemap_url',
        default=None,
        help='URL of the target sitemap',
        type=str)
    parser.add_argument(
        '--twitter_user_id',
        default=None,
        help='User id of your twitter account, i.e. your twitter handle without `@`.',
        type=str)
    args = parser.parse_args()
    main(args)
