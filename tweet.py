import os
import tweepy

from llm import ClarifaiPrompter

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


def clean_llm_output(raw_text: str) -> str:
    cleaned = raw_text.split('\n\n')[1]
    cleaned = cleaned.replace("example", "")
    return cleaned

def main():

    prompter = ClarifaiPrompter()
    output = prompter.predict()

    tweet = clean_llm_output(output)

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    response = client.create_tweet(
        text=tweet
    )
    print(response.status_code)

if __name__ == "__main__":
    main()