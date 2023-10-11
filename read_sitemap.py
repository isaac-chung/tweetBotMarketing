import requests
import pandas as pd
import random
import xmltodict

from constants import PROMPT_TEMPLATE
from llm import ClarifaiPrompter


YEAR_ONWARDS = 2023
SITEMAP_URL = "https://www.clarifai.com/sitemap.xml"
LASTMOD = "lastmod"

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
    output = p.predict(prompt)
    print(output)



if __name__ == "__main__":
    main()
