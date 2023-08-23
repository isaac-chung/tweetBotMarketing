import os
import random

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from constants import USER_ID, APP_ID, MODEL_ID, MODEL_VERSION_ID, PROMPTS

class ClarifaiPrompter:
    def __init__(self):
        self.prompt = random.choice(PROMPTS)
        self.userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
        self.metadata = (('authorization', 'Key ' + os.environ.get("CLARIFAI_PAT_PROD")),)

        channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(channel)

    def predict(self, model_id=MODEL_ID, model_version_id=MODEL_VERSION_ID) -> str:
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=model_id,
                version_id=model_version_id, 
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=self.prompt
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        return post_model_outputs_response.outputs[0].data.text.raw
    

def main():
    prompter = ClarifaiPrompter()
    output = prompter.predict()
    print(output)

if __name__ == "__main__":
    main()