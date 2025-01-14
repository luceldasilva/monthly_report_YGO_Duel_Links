from fastapi import APIRouter, HTTPException, status
from db.models.circular_card_images import ImageCharacter
from db.schemas.character import playable_characters_schema, characters_schema
from config.cfg import character_collections


characters = APIRouter(
    prefix="/characters",
    tags=["characters"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado :'v"}}
)


def search_character(field: str, key):
    try:
        features_character = character_collections.find_one({field: key})
        return ImageCharacter(**playable_characters_schema(features_character))
    except:
        return {"error": "No están las características que buscas"}


@characters.get("/", response_model=list[ImageCharacter])
async def all_characters():
    return characters_schema(character_collections.find())


@characters.get("/{character}", response_model=ImageCharacter)
async def searching_by_playable_character(name_character: str):
    return search_character("character_name", name_character)


@characters.post("/", response_model=ImageCharacter, status_code=status.HTTP_201_CREATED) 
async def save_playable_character(playable_character: ImageCharacter):
    
    if type(search_character("character_name", playable_character.character_name)) == ImageCharacter:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ey, el personaje ya tiene imagen"
        )
    
    if type(search_character("url_image", playable_character.url_image)) == ImageCharacter:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ey, La imagen ya la tiene otro personaje, revíselo"
        )
    
    character_dict = dict(playable_character)
    del character_dict["id"]
    
    id = character_collections.insert_one(character_dict).inserted_id 
    new_character = playable_characters_schema(character_collections.find_one({"_id":id}))
    
    return ImageCharacter(**new_character)


@characters.delete("/{character}", status_code=status.HTTP_204_NO_CONTENT)
async def drop_playable_character(character: str):
    
    found = character_collections.find_one_and_delete({"name": character})
    
    if not found: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El arquetipo no existe"
        )
