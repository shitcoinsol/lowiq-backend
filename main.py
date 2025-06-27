from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import openai, shutil, os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_image(file: UploadFile = File(...)):
    try:
        with open("input.png", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        response = openai.images.generate(
            model="dall-e-3",
            prompt="Generate a cartoon character with a silly face",  # 테스트용 간단 프롬프트
            size="1024x1024",
            response_format="url",
            n=1
        )
        return { "image_url": response['data'][0]['url'] }
    except Exception as e:
        return { "error": str(e) }
