import csv
from pathlib import Path
from typing import List

from tibcleaner.config import DATA_DIR


def get_all_doc_files(folder_dir: Path):
    """some of the doc files have space in btw so rename them to TX0, TX1, TX2, ... TXn"""
    files = list(folder_dir.rglob("*.doc"))
    return rename_doc_files(files, Path(f"file_mapping_{folder_dir.name}_folder.csv"))


def rename_doc_files(file_paths: List[Path], csv_file_path: Path):
    renamed_files = []
    # Open a CSV file for writing the mapping of old and new filenames
    with open(csv_file_path, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Old Filename", "New Filename"])  # Header

        for i, file_path in enumerate(file_paths):
            new_file_path = file_path.parent / f"TX{i}.doc"
            file_path.rename(new_file_path)
            renamed_files.append(new_file_path)
            csvwriter.writerow([file_path, new_file_path])

    return renamed_files


if __name__ == "__main__":
    doc_path = DATA_DIR
    print(get_all_doc_files(doc_path))
