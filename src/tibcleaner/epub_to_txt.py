# importing libraries
from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from tqdm import tqdm

from tibcleaner.checkpoint import (
    load_checkpoints,
    save_checkpoint,
    save_corrupted_files,
)


def _mkdir(path: Path) -> Path:
    if path.is_dir():
        return path
    path.mkdir(exist_ok=True, parents=True)
    return path


def epub_to_txt(epub_path: Path, output_dir: Path) -> None:
    try:
        # Ensure output directory exists
        _mkdir(output_dir)
        # Load the EPUB file
        book = epub.read_epub(epub_path)
        full_text = ""

        # Iterate through each document in the EPUB file
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Use BeautifulSoup to extract text
                soup = BeautifulSoup(item.content, "html.parser")
                text = soup.get_text()
                # Append the text to the full_text variable, with some spacing
                full_text += "\n\n" + text

        # Write the extracted text to a new TXT file
        output_txt_path = output_dir / (epub_path.name + ".txt")
        with open(output_txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(full_text)

        # If everything went well, save the epub_path to the checkpoint
        save_checkpoint(epub_path)
    except Exception as e:
        # If there was an error, log the epub_path to the corrupted files log
        print(f"Error processing {epub_path}: {e}")
        save_corrupted_files(epub_path, f"Error processing {epub_path}: {e}")


if __name__ == "__main__":
    output_dir = Path("/root/epub_to_txt/A/")
    epub_files = list(Path("/root/A/").rglob("*.epub"))
    _mkdir(output_dir)
    checkpoints = load_checkpoints()
    for epub_file in tqdm(epub_files, desc="Converting TXT to txt"):
        if str(epub_file) in checkpoints:
            continue
        epub_to_txt(epub_file, output_dir)
