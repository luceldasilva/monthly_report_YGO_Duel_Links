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
    try:
        features_archetype = deck_collections.find_one({field: key})
        return ImageCard(**archetype_schema(features_archetype))
    except:
        return {"error": "No están las características que buscas"}


@decks.get("/", response_model=list[ImageCard])
async def all_decks():
    return decks_schema(deck_collections.find())


@decks.get("/{deck}", response_model=ImageCard)
async def searching_by_archetype(name_deck: str):
    return search_deck("name", name_deck)


@decks.post("/", response_model=ImageCard, status_code=status.HTTP_201_CREATED) 
async def save_archetype(archetype: ImageCard):
    
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
    
    found = deck_collections.find_one_and_delete({"name": deck})
    
    if not found: 
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="El arquetipo no existe"
        )


@decks.patch("/", response_model=ImageCard)
async def update_archetype(archetype: CardUpdate):
    
    if not type(search_user("name", archetype.name)) == ImageCard: # type: ignore
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Ese deck no existe"
        )
    
    deck_dict = dict(archetype)
    del deck_dict["id"]
    
    try:        
        deck_collections.find_one_and_update(
            {"name": archetype.name},
            {"$set": archetype.dict(exclude_none=True)},
            return_document=ReturnDocument.AFTER
        )
    except:
        return {"error": "No se ha actualizado el arquetipo"}
    
    return CardUpdate(archetype.name)