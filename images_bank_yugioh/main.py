from fastapi import FastAPI
from config.docs import tags_metadata
from routers import cloudinary_bank, images_decks


app = FastAPI(
    title="Banco de Imágenes para arquetipos de Yu-Gi-Oh!",
    description="Avatares para hacer referencia a los mazos",
    openapi_tags=tags_metadata,
    version="1.0.2"
)


@app.get("/")
async def root():
    return {"message": "ola k ase"}


app.include_router(cloudinary_bank.circular_images)
app.include_router(images_decks.decks)