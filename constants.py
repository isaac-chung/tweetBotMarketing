from string import Template

## For the LLM Prompting
USER_ID = 'meta'
APP_ID = 'Llama-2'
MODEL_ID = 'llama2-70b-chat'
MODEL_VERSION_ID = '6c27e86364ba461d98de95cddc559cb3'

PROMPT_TEMPLATE = Template("Prepare a tweet to promote $highlight. Only output the raw text of the tweet without any instructions or any preamble. Include the hashtags '$hashtags'. Include the relevant link $optional `$link`. Limit the tweet to 260 characters including the link.")
PROMOTION_HASHTAG_LINK_TUPLES = [
    ("Clarifai's LLM finetuning capabilities", "#llms", "to a blogpost", "https://www.clarifai.com/blog/fine-tuning-gpt-neo-for-text-classification"),
    ("100 Clarifai hackathon projects", "#ai", "to a blogpost", "https://www.clarifai.com/blog/100-clarifai-hackathon-projects-from-2018"),
    ("generative AI", "#genai", "to a blogpost", "https://www.clarifai.com/blog/generative-ai-and-large-language-models"),
    ("running code llama on Clarifai", "#ai #llms", "", "https://www.clarifai.com/blog/run-code-llama-with-an-api-1"),
    ("Clarifai's LLM finetuning capabilities", "#llms", "to a video tutorial", "https://www.youtube.com/watch?v=Ycl7xVA2wHk"),
    ("Clarifai's vector search capabilities", "#llms", "", "https://www.clarifai.com/use-cases/visual-search"),
    ("Clarifai's generative AI capabilities", "#generativeAI", "", "https://www.clarifai.com/products/generative-ai"),
    ("Clarifai's content moderation capabilities", "#llms", "", "https://www.clarifai.com/solutions/content-moderation"),
    ("Clarifai's DAM capabilities", "#Clarifai", "", "https://www.clarifai.com/solutions/digital-asset-management"),
    ("Clarifai's predictive maintenance capabilities", "#Clarifai", "", "https://www.clarifai.com/use-cases/predictive-maintenance"),
    ("Clarifai's Edge AI capabilities", "#Clarifai", "", "https://www.clarifai.com/use-cases/isr-edge-ai"),
    ("Clarifai's open positions", "#hiring", "", "https://www.clarifai.com/company/careers"),
    ("Clarifai's LLM prompt capabilities", "#llms", "", "https://docs.clarifai.com/api-guide/predict/llms/#via-raw-text"),
    ("Clarifai's serverless inference capabilities", "#llms", "", "https://docs.clarifai.com/api-guide/predict/llms/#via-raw-text"),
    ("a Clarifai customer Acquia DAM", "#llms", "", "https://www.clarifai.com/customers/acquia-dam"),
    ("a Clarifai customer that is a business retailer", "#llms", "", "https://www.clarifai.com/customers/business-retailer"),
    ("a Clarifai customer Foap", "#llms", "", "https://www.clarifai.com/customers/foap"),
    ("a Clarifai customer that is a DAM company", "#llms", "", "https://www.clarifai.com/customers/dam-company"),
    ("a Clarifai customer that is a leading online travel booking site", "#llms", "", "https://www.clarifai.com/customers/online-travel-agency"),
    ("a Clarifai customer that is an international mobile app company", "#llms", "", "https://www.clarifai.com/customers/mobile-phone-app"),
    ("a Clarifai customer OpenTable", "#llms", "", "https://www.clarifai.com/customers/opentable"),
    ("a Clarifai customer 9GAG", "#llms", "", "https://www.clarifai.com/customers/9gag"),
    ("a Clarifai customer that is a Fortune 100 retailer", "#llms", "", "https://www.clarifai.com/customers/home-improvement-retailer"),
    ("Clarifai's hosted AI foundation models", "#llms", "", "https://www.clarifai.com/blog/choosing-best-foundation-model-for-your-use-case"),
    ("Clarifai's bulk labeling capabilities", "#AI #labeling", "", "https://www.clarifai.com/blog/bulk-labeling-the-fast-and-easy-way")
]

PROMPTS = [
    PROMPT_TEMPLATE.safe_substitute(
        highlight=tup[0], 
        hashtags=tup[1],
        optional=tup[2],
        link=tup[3]
    ) for tup in PROMOTION_HASHTAG_LINK_TUPLES
]

## For building the HTML
TWITTER_USER_ID='i48456'

## For uploading the screenshot to clarifai
UPLOAD_USER_ID = 'Isaac'
UPLOAD_APP_ID = 'tweet-screenshots'
