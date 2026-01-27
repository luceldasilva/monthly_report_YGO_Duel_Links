from fastapi import APIRouter, HTTPException, status
from db.models.circular_card_images import ImageCharacter, CharacterUpdate
from db.schemas.character import playable_characters_schema, characters_schema
from config.cfg import character_collections
from pymongo.collection import ReturnDocument


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
    """
    Muestra todos los personajes

    Returns
    -------
    dict:
        Los personajes con su id y avatares
    """
    return characters_schema(character_collections.find())


@characters.get("/{character}", response_model=ImageCharacter)
async def searching_by_playable_character(character: str):
    """
    Búsqueda del personaje en concreto

    Parameters
    ----------
    name_character : str
        nombre del personaje

    Returns
    -------
    dict:
        Su documento completo con su id y url del avatar
    
    Raises
    ------
    HTTPException
        Por si ese personaje con ese nombre no está en la base de datos
    """
    
    if not type(search_character("character_name", character)) == ImageCharacter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ese personaje no existe"
        )
    return search_character("character_name", character)


@characters.post("/", response_model=ImageCharacter, status_code=status.HTTP_201_CREATED) 
async def save_playable_character(playable_character: ImageCharacter):
    """
    Añadir nuevo personaje

    Parameters
    ----------
    playable_character : ImageCharacter
        Se agrega con su id, nombre y el url del avatar

    Returns
    -------
    dict: 
        Muestra su documentación completa

    Raises
    ------
    HTTPException
        Por si ese nombre ya está en la base de datos
    HTTPException
        Por si la url del avatar ya está en está en la base de datos
    """
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
    """
    Borrar personaje

    Parameters
    ----------
    character : str
        Nombre del personaje

    Raises
    ------
    HTTPException
        Por si ese nombre no existe
    """
    found = character_collections.find_one_and_delete({"character_name": character})
    
    if not found: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El personaje no existe"
        )


@characters.patch("/", response_model=ImageCharacter)
async def update_archetype(playable: CharacterUpdate):
    """
    Parameters
    ----------
    archetype : CharacterUpdate
        Actualizar el avatar del personaje, obligado el nombre y la url nueva

    Raises
    ------
    HTTPException
        Por si el nombre no existe en el documento
    """
    
    if not type(search_character("character_name", playable.character_name)) == ImageCharacter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ese personaje no existe"
        )
    
    character_dict = dict(playable)
    del character_dict["id"]
    
    try:        
        character_collections.find_one_and_update(
            {"character_name": playable.character_name},
            {"$set": playable.model_dump(exclude_none=True)},
            return_document=ReturnDocument.AFTER
        )
    except:
        return {"error": "No se ha actualizado el arquetipo"}
    
    return search_character("character_name", playable.character_name)
