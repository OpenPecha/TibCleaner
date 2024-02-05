from pathlib import Path
from typing import List

from tibcleaner.config import DATA_DIR


def get_all_doc_files(folder_dir: Path):
    """some of the doc files have space in btw so rename them to TX0, TX1, TX2, ... TXn"""
    files = list(folder_dir.rglob("*.doc"))
    return rename_doc_files(files)


def rename_doc_files(file_paths: List[Path]):
    renamed_files = []
    for i, file_path in enumerate(file_paths):
        file_path.rename(file_path.parent / f"TX{i}.doc")
        renamed_files.append(Path(file_path.parent / f"TX{i}.doc"))
    return renamed_files


if __name__ == "__main__":
    doc_path = DATA_DIR
    print(get_all_doc_files(doc_path))
