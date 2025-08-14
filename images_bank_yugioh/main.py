from fastapi import FastAPI
from config.docs import tags_metadata
from routers import cloudinary_bank, images_decks, playable_characters


app = FastAPI(
    title="Banco de Imágenes para arquetipos de Yu-Gi-Oh!",
    description="Avatares para hacer referencia a los mazos y personajes",
    openapi_tags=tags_metadata,
    version="1.3.0"
)


@app.get("/")
async def root():
    """
    Página de inicio

    Returns
    -------
    dict:
        mensaje de bienvenida
    """
    return {"message": "La baraja de mi abuelo no tiene cartas patéticas, Kaiba. Pero contiene... ¡la imparable Exodia!"}


app.include_router(cloudinary_bank.circular_images)
app.include_router(images_decks.decks)
app.include_router(playable_characters.characters)