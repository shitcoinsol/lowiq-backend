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
    with open("input.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    response = openai.images.generate(
        model="dall-e-3",
        prompt="""Transform only the face and head of the subject in the image into a ‘LowIQ’ meme-style character.
Give them an oversized, slightly deformed bald head, asymmetrical and awkwardly shaped.
The eyes must have no focus — pointing in different directions with large visible white space.
Keep the mouth open at all times, with a silly drooling expression. Blue saliva should drip down.
Maintain the original skin tone of the subject exactly as in the original image.
The original clothing should remain, but a "LOWIQ" badge must be visibly attached and rendered in the same distorted style.
Use a cartoonish, hand-drawn illustration look, with shaky lines, no shading, and flat pastel or garish colors.
Only modify the face and clothing label; background and pose must stay unchanged. 512x512 size.
""", 
        size="1024x1024",
        response_format="url",
        n=1
    )
    return { "image_url": response['data'][0]['url'] }
