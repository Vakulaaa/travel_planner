from typing import Any

import requests

AIC_API_ARTWORK_URL = "https://api.artic.edu/api/v1/artworks/{external_id}"


class PlaceValidationError(Exception):
    pass


def get_artwork_by_external_id(external_id: int) -> dict[str, Any]:
    response = requests.get(
        AIC_API_ARTWORK_URL.format(external_id=external_id),
        timeout=10,
    )

    if response.status_code != 200:
        raise PlaceValidationError("Place was not found in Art Institute API.")

    payload = response.json()
    data = payload.get("data")
    if not data:
        raise PlaceValidationError("Place data is missing in Art Institute API response.")

    return data
