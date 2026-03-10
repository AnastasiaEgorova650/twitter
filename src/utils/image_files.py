import os
from contextlib import suppress
from datetime import datetime
from http import HTTPStatus

import aiofiles
from fastapi import UploadFile
from loguru import logger
from starlette.exceptions import HTTPException

from src.core.config import ALLOWED_EXTENSIONS, IMAGES_FOLDER, STATIC_FOLDER


def allowed_image(image_name: str) -> None:
    if (
        "." in image_name
        and image_name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    ):
        logger.info("Формат изображения корректный")
    else:
        logger.error("Неразрешенный формат изображения")

        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,  # 422
            detail=f"Разрешенные форматы изображений: {ALLOWED_EXTENSIONS}",
        )


def clear_path(path: str) -> str:
    return path.split("static")[1][1:]


async def create_directory(path: str) -> None:
    logger.debug(f"Создание директории: {path}")
    os.makedirs(path)


async def writing_file_to_hdd(image_file: UploadFile) -> str:
    allowed_image(image_name=image_file.filename)

    with suppress(OSError):
        logger.debug("Сохранение изображения к твиту")
        current_date = datetime.now()
        path = os.path.join(
            IMAGES_FOLDER,
            "tweets",
            f"{current_date.year}",
            f"{current_date.month}",
            f"{current_date.day}",
        )

        if not os.path.isdir(path):
            await create_directory(path=path)

        img_contents = image_file.file.read()
        full_path = os.path.join(path, f"{image_file.filename}")

        async with aiofiles.open(full_path, mode="wb") as img_file:
            await img_file.write(img_contents)

    return clear_path(path=full_path)


async def delete_image_from_hdd(images):
    logger.debug("Удаление изображений из файловой системы")
    try:
        os.remove(os.path.join(STATIC_FOLDER, images[0].path_media))
    except FileNotFoundError:
        logger.debug(f"Файл {images[0].path_media} не найден")
    logger.debug(f"Изображение - {images[0].path_media} удалено")
