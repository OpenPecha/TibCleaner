"""function to extract zip files"""

import zipfile
from pathlib import Path
from typing import List

import rarfile
from tqdm import tqdm


def extract_zip_files(zip_file_paths: List[Path], destination_dir: Path):
    destination_dir.mkdir(parents=True, exist_ok=True)

    for zip_path in tqdm(zip_file_paths, desc="Extracting ZIP files"):
        if zip_path.suffix == ".zip":
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(destination_dir / zip_path.stem)


def extract_rar_files(rar_file_paths: List[Path], destination_dir: Path):
    destination_dir.mkdir(parents=True, exist_ok=True)

    for rar_path in tqdm(rar_file_paths, desc="Extracting RAR files"):
        if rar_path.suffix == ".rar":
            with rarfile.RarFile(rar_path, "r") as rar_ref:
                rar_ref.extractall(destination_dir / rar_path.stem)


if __name__ == "__main__":
    data_dir = Path("/root/A")
    destination_dir = Path("/root/A_ZIP")
    rar_files = list(data_dir.rglob("*.rar"))
    zip_files = list(data_dir.rglob("*.zip"))
    extract_zip_files(zip_files, destination_dir)
    extract_rar_files(rar_files, destination_dir)

    print("Extraction complete")
