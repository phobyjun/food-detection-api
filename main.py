from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from app.food_detection import detect_with_clarifai, HttpStatusCodeException

CFG = dotenv_values(".env")
api_key = CFG["API_KEY"]
api_url = CFG["API_URL"]
clarifai_api_key = CFG["CLARIFAI_API_KEY"]
clarifai_model_id = CFG["CLARIFAI_MODEL_ID"]

app = FastAPI()


@app.get("/food/health-check", status_code=200)
async def health_check():
    return {"status": "success"}


base_s3_route = "https://naeng-bu-test.s3.ap-northeast-2.amazonaws.com/"


@app.get("/food/{image_url}")
async def food_detection_api(image_url: str):
    img_url = base_s3_route + image_url
    try:
        food = detect_with_clarifai(img_url, clarifai_api_key, clarifai_model_id)
    except HttpStatusCodeException as error:
        return HTTPException(500, detail=error)

    return {
        "food": food
    }


handler = Mangum(app)
