import csv
from pathlib import Path
from typing import List


def get_all_files(folder_dir: Path, dir_name: str) -> List[Path]:
    file_formats = ["file_extension1", "file_extension2"]
    files: List[Path] = []  # Type annotation added here

    for file_format in file_formats:
        files.extend(folder_dir.rglob(f"*.{file_format}"))

    print(f"Found {len(files)} files.")
    csv_file_path = f"{dir_name}_renamed_files.csv"
    return rename_files(files, csv_file_path, dir_name)


def rename_files(
    file_paths: List[Path], csv_file_path: str, dir_name: str
) -> List[Path]:
    renamed_files: List[Path] = []  # Ensuring type annotations for clarity
    with open(csv_file_path, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Old Filename", "New Filename"])

        for i, file_path in enumerate(file_paths):
            original_extension = file_path.suffix
            new_file_path = file_path.parent / f"{dir_name}_{i:07}{original_extension}"
            file_path.rename(new_file_path)
            renamed_files.append(new_file_path)

            csvwriter.writerow([str(file_path), str(new_file_path)])

    print(f"Renamed {len(renamed_files)} files.")
    return renamed_files


if __name__ == "__main__":
    folder_dir = Path("root/A")
    dir_name = "A"
    get_all_files(folder_dir, dir_name)
