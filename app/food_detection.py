import requests
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from dotenv import dotenv_values

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())


class HttpStatusCodeException(Exception):
    def __init__(self, msg, status_code):
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return self.msg

    def status_code(self):
        return self.status_code


# TODO: API 권한 문제
def detect_with_food_ai(_image_url, _api_key, _api_url) -> str:
    request_params = {
        "image_url": _image_url,
        "num_tag": 10,
        "api_key": _api_key,
        "longitude": 127,
        "latitude": 37
    }
    resp = requests.post(_api_url, json=request_params)
    resp_json = resp.json()

    status_code = resp_json["status_code"]
    status_msg = resp_json["status_msg"]
    if status_code != 200:
        raise HttpStatusCodeException(
            msg=status_msg, status_code=status_code
        )

    return resp.json()["food_results"][0][0]


def detect_with_clarifai(_image_url, _api_key, _model_id) -> str:
    metadata = (('authorization', f'Key {_api_key}'),)

    request = service_pb2.PostModelOutputsRequest(
        model_id=_model_id,
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(
                image=resources_pb2.Image(url=_image_url)
            ))
        ])
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise HttpStatusCodeException(
            msg=response.status.description, status_code=response.status.code
        )

    return response.outputs[0].data.concepts[0].name


if __name__ == "__main__":
    cfg = dotenv_values(".env")
    image_url = "https://naeng-bu-test.s3.ap-northeast-2.amazonaws.com/banana.jpeg"
    api_key = cfg["API_KEY"]
    api_url = cfg["API_URL"]
    detect_with_food_ai(image_url, api_key, api_url)

    clarifai_api_key = cfg["CLARIFAI_API_KEY"]
    clarifai_model_id = cfg["CLARIFAI_MODEL_ID"]
    detected = detect_with_clarifai(image_url, clarifai_api_key, clarifai_model_id)
    print(detected)
