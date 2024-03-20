import shutil
from pathlib import Path


def copy_txt_files(source_dir: Path, destination_dir: Path) -> None:
    """
    Copies all .txt files from source_dir to destination_dir, including subdirectories.
    Does not overwrite existing files with the same name in the destination.

    :param source_dir: Path object representing the source directory.
    :param destination_dir: Path object representing the destination directory.
    """
    # Ensure the destination directory exists
    destination_dir.mkdir(parents=True, exist_ok=True)

    # Use rglob to find all .txt files in the source directory and its subdirectories
    for txt_file in source_dir.rglob("*.txt"):
        # Construct the destination file path
        destination_file_path = destination_dir / txt_file.name

        # Check if a file with the same name already exists in the destination
        if not destination_file_path.exists():
            # Copy the text file to the destination directory
            shutil.copy(txt_file, destination_file_path)

    print("All text files have been copied to the destination folder.")


# Example usage
if __name__ == "__main__":
    source_dir = Path("/root/A")
    destination_dir = Path("/root/txt/A")
    copy_txt_files(source_dir, destination_dir)
