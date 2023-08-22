import json
import os
import random
import requests

from clarifai_grpc.grpc.api.status import status_code_pb2

from constants import USER_ID, APP_ID, MODEL_ID, MODEL_VERSION_ID, PROMPTS

class ClarifaiPrompter:
    def __init__(self):
        self.prompt = random.choice(PROMPTS)

    def predict(self, model_id=MODEL_ID, model_version_id=MODEL_VERSION_ID) -> str:

        url = f"https://api.clarifai.com/v2/users/{USER_ID}/apps/{APP_ID}/models/{model_id}/versions/{model_version_id}/outputs"
        payload = json.dumps({
            "inputs": [
                {
                    "data": {
                        "text": {
                            "raw": self.prompt
                        }
                    }
                }
            ]
        })
        headers = {
            'Authorization': 'Key %s' % os.environ.get("CLARIFAI_PAT_PROD"),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()

        if response['status']['code'] != status_code_pb2.SUCCESS:
            print(response['status'])
            raise Exception("Post model outputs failed, status: " + response['status']['description'])

        return response['outputs'][0]['data']['text']['raw']
    

def main():
    prompter = ClarifaiPrompter()
    output = prompter.predict()
    print(output)

if __name__ == "__main__":
    main()