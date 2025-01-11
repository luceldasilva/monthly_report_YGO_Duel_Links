from pydantic import BaseModel
from datetime import datetime
from pytz import timezone
from typing import Optional


"""
TODO: hacer clase para personajes a la misma estructura que los decks
"""

now = datetime.now(timezone('America/Eirunepe'))
registry = now.strftime('%d-%m-%Y')


class ImageCard(BaseModel):
    id: Optional[str] = None
    name: str
    url_image: str
    update_image_at: str = 'no prior registration'


class CardUpdate(BaseModel):
    id: Optional[str] = None
    name: str
    url_image: str
    update_image_at: str = registry