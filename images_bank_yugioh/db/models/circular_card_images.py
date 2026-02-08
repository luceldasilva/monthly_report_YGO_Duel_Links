from config.cfg import URL_DEFAULT
from pydantic import BaseModel
from datetime import datetime
from pytz import timezone
from typing import Optional


now = datetime.now(timezone('America/Eirunepe'))
registry = now.strftime('%d-%m-%Y')


class ImageCard(BaseModel):
    id: Optional[str] = None
    deck_id: int
    name: str
    url_image: str
    big_avatar: str = URL_DEFAULT
    update_image_at: str = 'no prior registration'


class CardUpdate(BaseModel):
    id: Optional[str] = None
    deck_id: Optional[int] = None
    name: str
    url_image: Optional[str] = None
    big_avatar: Optional[str] = None
    update_image_at: str = registry


class ImageCharacter(BaseModel):
    id: Optional[str] = None
    character_id: int
    character_name: str
    url_image: str
    update_image_at: str = 'no prior registration'


class CharacterUpdate(BaseModel):
    id: Optional[str] = None
    character_id: Optional[int] = None
    character_name: str
    url_image: str
    update_image_at: str = registry