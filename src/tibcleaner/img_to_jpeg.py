from pathlib import Path
from typing import List, cast

from PIL import Image
from tqdm import tqdm

from tibcleaner.checkpoint import (
    load_checkpoints,
    save_checkpoint,
    save_corrupted_files,
)


def _mkdir(path):
    if path.is_dir():
        return path
    path.mkdir(exist_ok=True, parents=True)
    return path


def convert_image_format_to_jpeg(image_path: Path, destination_dir: Path):
    known_formats = ["png", "PCX", "jpg", "JPG", "gif", "tif", "TIF", "svg"]
    file_type = image_path.suffix[1:]
    if file_type in known_formats:
        try:
            with Image.open(image_path) as img:
                img = cast(Image.Image, img).convert("RGB")
                output_dir = destination_dir / file_type
                output_dir.mkdir(parents=True, exist_ok=True)
                image_path = output_dir / f"{image_path.stem}.jpeg"
                img.save(image_path, "JPEG")
                save_checkpoint(image_path)
                return image_path
        except Exception as e:
            save_corrupted_files(
                image_path, f"{str(image_path)} couldnt be converted to jpeg. {e}"
            )
            return None


if __name__ == "__main__":
    output_dir = Path("/root/img_to_jpeg/A/")

    """ Filtering the images and then removing the duplicates """
    image_formats = ["png", "PCX", "jpg", "JPG", "gif", "tif", "TIF", "svg"]
    files: List[Path] = []

    for image_format in image_formats:
        files.extend(Path("B").rglob(f"*.{image_format}"))
    _mkdir(output_dir)
    checkpoints = load_checkpoints()
    for file in tqdm(files, desc="Converting to jpeg"):
        if str(file) in checkpoints:
            continue
        convert_image_format_to_jpeg(file, output_dir)
