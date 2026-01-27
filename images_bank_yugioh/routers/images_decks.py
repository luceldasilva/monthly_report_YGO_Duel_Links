from fastapi import APIRouter, HTTPException, status
from db.models.circular_card_images import ImageCard, CardUpdate
from db.schemas.archetype import archetype_schema, decks_schema
from config.cfg import deck_collections
from pymongo.collection import ReturnDocument


decks = APIRouter(
    prefix="/decks",
    tags=["decks"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado :'v"}}
)


def search_deck(field: str, key):
    """Buscar características del mazo

    Parameters
    ----------
    field : str
        columna/s
    key : int | str

    Returns
    -------
    Devuelve el documento con las características que se pedía
    """
    try:
        features_archetype = deck_collections.find_one({field: key})
        return ImageCard(**archetype_schema(features_archetype))
    except:
        return {"error": "No están las características que buscas"}


@decks.get("/", response_model=list[ImageCard])
async def all_decks():
    """
    Muestra total del documento de los mazos

    Returns
    -------
    Todos los mazos con sus id's y avatares
    """
    return decks_schema(deck_collections.find())


@decks.get("/{deck}", response_model=ImageCard)
async def searching_by_archetype(deck: str):
    """
    Búsqueda del Arquetipo

    Parameters
    ----------
    name_deck : str
        Nombre del arquetipo

    Returns
    -------
    Te muestra su documento completo, con su id y avatar
    
    Raises
    ------
    HTTPException
        Ese nombre de arquetipo no existe
    """
    if not type(search_deck("name", deck)) == ImageCard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ese deck no existe"
        )
    return search_deck("name", deck)


@decks.post("/", response_model=ImageCard, status_code=status.HTTP_201_CREATED) 
async def save_archetype(archetype: ImageCard):
    """
    Agregar nuevo mazo 

    Parameters
    ----------
    archetype : ImageCard
        Se agrega con su deck_id, nombre y el url del avatar

    Returns
    -------
    dict:
        El documento ya formado con su información completa

    Raises
    ------
    HTTPException
        Si ya existe el arquetipo en cuestión
    HTTPException
        Si ya es la misma url ya presente en otro documento
    """
    if type(search_deck("name", archetype.name)) == ImageCard:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ey, el arquetipo ya tiene imagen"
        )
    
    if type(search_deck("url_image", archetype.url_image)) == ImageCard:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ey, La imagen ya la tiene otro arquetipo, revíselo"
        )
    
    deck_dict = dict(archetype)
    del deck_dict["id"]
    
    id = deck_collections.insert_one(deck_dict).inserted_id 
    new_deck = archetype_schema(deck_collections.find_one({"_id":id}))
    
    return ImageCard(**new_deck)


@decks.delete("/{deck}", status_code=status.HTTP_204_NO_CONTENT)
async def drop_archetype(deck: str):
    """
    Borrar el arquetipo de la base de datos

    Parameters
    ----------
    deck : str
        el nombre del arquetipo
    
    Returns
    -------
    dict:
        El documento ya formado con su información actualizada

    Raises
    ------
    HTTPException
        Por si ese nombre no existe en la data
    """
    found = deck_collections.find_one_and_delete({"name": deck})
    
    if not found: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El arquetipo no existe"
        )


@decks.patch("/", response_model=ImageCard)
async def update_archetype(archetype: CardUpdate):
    """
    Parameters
    ----------
    archetype : CardUpdate
        Actualizar el avatar del deck, obligado el nombre y la url nueva

    Raises
    ------
    HTTPException
        Por si el nombre no existe en el documento
    """
    if not type(search_deck("name", archetype.name)) == ImageCard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ese deck no existe"
        )
    
    deck_dict = dict(archetype)
    del deck_dict["id"]
    
    try:        
        deck_collections.find_one_and_update(
            {"name": archetype.name},
            {"$set": archetype.model_dump(exclude_none=True)},
            return_document=ReturnDocument.AFTER
        )
    except:
        return {"error": "No se ha actualizado el arquetipo"}
    
    return search_deck("name", archetype.name)