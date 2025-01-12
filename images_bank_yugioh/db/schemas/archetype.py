def archetype_schema(archetype) -> dict:
    return {
        "id": str(archetype["_id"]),
        "deck_id": archetype["deck_id"],
        "name": archetype["name"],
        "url_image": archetype["url_image"],
        "update_image_at": archetype["update_image_at"]
    }


def decks_schema(decks) -> list:
    return [archetype_schema(archetype) for archetype in decks]