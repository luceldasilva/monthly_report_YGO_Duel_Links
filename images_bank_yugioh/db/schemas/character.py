def playable_characters_schema(playable) -> dict:
    return {
        "id": str(playable["_id"]),
        "character_id": playable["character_id"],
        "character_name": playable["name"],
        "url_image": playable["url_image"],
        "update_image_at": playable["update_image_at"]
    }


def characters_schema(characters) -> list:
    return [playable_characters_schema(playable) for playable in characters]