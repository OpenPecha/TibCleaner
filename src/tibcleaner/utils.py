import shutil
from pathlib import Path
from typing import List

from tqdm import tqdm


def _mkdir(path: Path):
    """Ensure the directory exists."""
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)
    return path


def copy_documents(source_paths: List[Path], destination_dir: Path):
    # Ensure the destination directory exists
    destination_dir.mkdir(parents=True, exist_ok=True)

    # Iterate over each source path in the list
    for src_path in tqdm(source_paths, desc="copying files"):
        if src_path.is_file():
            # Construct the destination path
            dest_path = destination_dir / src_path.name

            shutil.copy(src_path, dest_path)
            print(f"Copied: {src_path} -> {dest_path}")
        else:
            print(f"Warning: Source path does not exist or is not a file: {src_path}")


def are_files_identical(file_path1: Path, file_path2: Path) -> bool:
    # First, check if the sizes are the same, as a quick preliminary check.
    if file_path1.stat().st_size != file_path2.stat().st_size:
        return False

    # Open both files and compare contents byte by byte.
    with file_path1.open("rb") as f1, file_path2.open("rb") as f2:
        while True:
            b1 = f1.read(4096)  # Read file in chunks of 4096 bytes
            b2 = f2.read(4096)

            if b1 != b2:
                return False  # Files differ

            if not b1:  # End of file reached
                return True  # Files are identical
