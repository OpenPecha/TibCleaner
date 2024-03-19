import csv
import zipfile
from pathlib import Path
from typing import List

from tqdm import tqdm

""" zip with renaming"""
""" safely extracting zip files"""
""" some of the files name were too long, so previous function faces some problems """
""" renaming files as DOC_H_ZIP_number.doc  """


def extract_zip_files(zip_file_paths: List[Path], destination_dir: Path, dir_name: str):
    destination_dir.mkdir(parents=True, exist_ok=True)
    mapping = []  # Store the mapping of old file names to new file names

    file_types_count = {}

    for zip_path in tqdm(zip_file_paths, desc="Extracting ZIP files"):
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for member in zip_ref.infolist():
                    original_file_name = member.filename
                    # Generate a unique short name for every file, regardless of length
                    file_type = Path(original_file_name).suffix

                    if not file_type:
                        continue

                    file_type = file_type[1:]

                    if file_type not in file_types_count:
                        file_types_count[file_type] = 1
                    else:
                        file_types_count[file_type] += 1

                    curr_file_type_count = file_types_count[file_type]
                    new_file_name = f"{file_type.upper()}_{dir_name}_{curr_file_type_count:07}.{file_type}"

                    # Record the mapping
                    mapping.append((original_file_name, new_file_name))

                    # Extract file with a new name
                    source = zip_ref.open(member)
                    target_file_path = destination_dir / new_file_name

                    with open(target_file_path, "wb") as target:
                        target.write(source.read())
                    source.close()
        except Exception as e:
            print(
                f"Warning: '{zip_path}' is not a valid ZIP file or is corrupted and will be skipped.{e}"
            )
    # Save the mapping to a CSV file
    mapping_csv_path = destination_dir / f"{dir_name}_filename_mapping.csv"
    with open(mapping_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Old File Name", "New File Name"])
        writer.writerows(mapping)
