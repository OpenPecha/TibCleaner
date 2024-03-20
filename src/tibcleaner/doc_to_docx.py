import time
from pathlib import Path

from doc2docx import convert
from tqdm import tqdm

checkpoint_file = "checkpoint.txt"
error_file = "errors.txt"

if not Path(checkpoint_file).exists():
    Path(checkpoint_file).touch()


def load_checkpoint():
    try:
        with open(checkpoint_file) as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


def add_checkpoint(file_name: str):
    with open(checkpoint_file, "a") as file:
        file.write(file_name + "\n")


def add_error(file_name: str, error: str):
    with open(error_file, "a") as file:
        file.write(f"{file_name}: {error}\n")


# Function to be executed by each worker in the pool
def convert_file(file_path: str):
    checkpoints = load_checkpoint()
    if file_path in checkpoints:
        print(f"Skipping {file_path} as it has already been converted")
        return
    try:
        start = time.time()
        convert(file_path, f"docx_output/{Path(file_path).stem}.docx")
        end = time.time()
        print(f"Converted {file_path} in {end - start:.2f} seconds")
        add_checkpoint(str(file_path))
    except Exception as e:
        add_error(str(file_path), str(e))
        print(f"Error converting {file_path}: {e}")


def main():
    # List all .doc files in the 'output' directory
    doc_files = [
        str(doc_file)
        for doc_file in Path("all_doc_files").rglob("*.doc")
        if doc_file.is_file()
    ]

    for doc_file in tqdm(doc_files, desc="converting doc to docx"):
        convert_file(doc_file)


if __name__ == "__main__":
    main()
