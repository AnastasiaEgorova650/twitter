import os
from http import HTTPStatus
from pathlib import Path

from httpx import AsyncClient

from tests.good_responses import image_load

_TEST_ROOT_DIR = Path(__file__).resolve().parents[1]

image_name = os.path.join(_TEST_ROOT_DIR, "tests", "image_for_test.jpg")
image = open(image_name, "rb")


async def test_add_image(ac: AsyncClient):
    response = await ac.post(
        "/api/medias", files={"file": image}, headers={"api-key": "test_1"}
    )
    img_data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert img_data == image_load

