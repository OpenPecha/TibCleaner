from pathlib import Path
from typing import List

from tibcleaner.img_to_jpeg import image_to_jpeg


def test_img_to_jpeg():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/img_to_jpeg")
    """ Filtering the images and then removing the duplicates """
    image_formats = [
        "png",
        "PCX",
        "jpg",
        "JPG",
        "gif",
        "tif",
        "TIF",
        "svg",
        "bmp",
        "BMP",
        "jpeg",
        "JPEG",
    ]
    files: List[Path] = []

    for image_format in image_formats:
        files.extend(folder_dir.rglob(f"*.{image_format}"))

    for img_file in files:
        file_type = img_file.suffix[1:]
        image_to_jpeg(img_file, output_dir)
        assert (output_dir / file_type / f"{img_file.stem}.jpeg").exists()
        (output_dir / file_type / f"{img_file.stem}.jpeg").unlink()
