# tweetBotMarketing

![Github Actions](https://github.com/chungisaac/tweetBotMarketing/actions/workflows/tweet.yml/badge.svg) [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

Reads the sitemap of a target website and generates tweets based on stored prompts. Optionally takes a screenshot of the tweet and uploads as an image to the Clarifai platform.

1. A random URL is chosen from the target sitemap
2. Calls GPT-4 to generate a tweet based on the cleaned URL and a random system prompt. That way the tweet would be in Chinese, Spanish, or in Pirate talk.
3. Posts the valid tweet on twitter via tweepy (require twitter crendentials)
4. Takes a screenshot of the tweet based on the tweet URL
5. Upload the screenshot to the clarifai platform to a specific user and app

## Pre-requisites

Sign up for a Twitter developer account and access your keys and secrets via https://developer.twitter.com/en/portal/dashboard. You will need
- consumer_key
- consumer_secret
- access_token
- access_token_secret

To call GPT-4, use Clarifai. Sign up for a free account and get a personal access token (PAT) via https://clarifai.com/settings/security. Set that as `CLARIFAI_PAT_PROD` (either as env var or repository secret).

## Usage

Use this by either running the script locally or via Github Actions after forking this repository. For both options, replace the following
- constants.py TWITTER_USER_ID

Install the requirements by running
```
pip install -r requirements.txt
```

Setup secrets and keys (see subsections below). Afterwards, run the scripts as such:
```
python read_sitemap.py --sitemap_url URL \
--twitter_user_id USER_HANDLE \
--screenshot_and_upload True
```

### Local
Set your secret and keys as environment variables, e.g.
```
export CONSUMER_KEY=your_consumer_key
```

### Github Actions

Follow these steps to setup your repository:
1. Fork this repository
2. Go to Settings -> Security -> Secrets and variables -> Actions
3. For each key/secret, click "New repository secret"
4. e.g. for the name, enter in all caps: CONSUMER_KEY. Then fill in your actual key in the "secret" text box. Click "Add secret"

Adjust how often you want to run the script via `.github/workflows/tweet.yml`. Github actions use cron expressions. e.g. `"20 */6 * * *"` means every 6 hours on the 20th minute on every day, every month, and every day of the week. I use [crontab guru](https://crontab.guru/) to help translate that.
