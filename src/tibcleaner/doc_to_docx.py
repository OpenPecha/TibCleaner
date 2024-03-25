# make sure to run windows os.
import time
from pathlib import Path

from doc2docx import convert
from tqdm import tqdm

from tibcleaner.checkpoint import (
    load_checkpoints,
    save_checkpoint,
    save_corrupted_files,
)


def doc_to_docx(file_path: str):
    checkpoints = load_checkpoints()
    if file_path in checkpoints:
        print(f"Skipping {file_path} as it has already been converted")
        return
    try:
        start = time.time()
        convert(file_path, f"docx_output/{Path(file_path).stem}.docx")
        end = time.time()
        print(f"Converted {file_path} in {end - start:.2f} seconds")
        save_checkpoint(Path(file_path))
    except Exception as e:
        save_corrupted_files(Path(file_path), str(e))
        print(f"Error converting {file_path}: {e}")


def main():
    # List all .doc files in the 'output' directory
    doc_files = [
        str(doc_file)
        for doc_file in Path("all_doc_files").rglob("*.doc")
        if doc_file.is_file()
    ]

    for doc_file in tqdm(doc_files, desc="converting doc to docx"):
        doc_to_docx(doc_file)


if __name__ == "__main__":
    main()
