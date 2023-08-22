## For the LLM Prompting
USER_ID = 'meta'
APP_ID = 'Llama-2'
MODEL_ID = 'llama2-70b-chat'
MODEL_VERSION_ID = '6c27e86364ba461d98de95cddc559cb3'

PROMPTS = [
    "Prepare a tweet to promote Clarifai's hackathon. Only output the raw text of the example. Do not include instructions. Include the hashtag '#Clarifai'. Limit the entire example to 220 characters. The registration link is https://lablab.ai/event/llama-2-hackathon-with-clarifai. Include it as well.",
    "Prepare a tweet to promote Clarifai's LLM finetuning capabilities. Only output the raw text of the example. Do not include instructions. Include the hashtag '#Clarifai'. Include the relevant link to a blogpost: 'https://www.clarifai.com/blog/fine-tuning-gpt-neo-for-text-classification'. Limit the entire example to 240 characters.",
    "Prepare a tweet to promote Clarifai's LLM finetuning capabilities. Only output the raw text of the example. Do not include instructions. Include the hashtag '#Clarifai'. Include the relevant link to a video tutorial: 'https://www.youtube.com/watch?v=Ycl7xVA2wHk'. Limit the entire example to 240 characters.",
    "Prepare a tweet to promote Clarifai's vector search capabilities. Only output the raw text of the example. Do not include instructions. Include the hashtag '#Clarifai'. Limit the entire example to 260 characters."
]

## For building the HTML
TWITTER_USER_ID='i48456'

## For uploading the screenshot to clarifai
UPLOAD_USER_ID = 'Isaac'
UPLOAD_APP_ID = 'tweet-screenshots'
