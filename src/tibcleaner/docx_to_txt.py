# importing libraries
from pathlib import Path

import docx
from tqdm import tqdm

from tibcleaner.checkpoint import (
    load_checkpoints,
    save_checkpoint,
    save_corrupted_files,
)
from tibcleaner.utils import _mkdir


def docx_to_txt(file_path: Path, output_dir: Path):
    """Converts a DOCX file to a TXT file."""
    _mkdir(output_dir)
    output_file = output_dir / f"{file_path.stem}.txt"
    try:
        # Load the .docx file
        doc = docx.Document(file_path)
    except Exception as e:
        save_corrupted_files(file_path, str(e))
        return None
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    text = "\n".join(fullText)

    # Write the content to a .txt file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)
    save_checkpoint(file_path)

    return output_file


if __name__ == "__main__":
    output_dir = Path("/root/docx_to_txt/A/")
    files = list(Path("/root/A/").rglob("*.docx"))
    _mkdir(output_dir)
    checkpoints = load_checkpoints()
    for file in tqdm(files, desc="Converting to txt"):
        if str(file) in checkpoints:
            continue
        docx_to_txt(file, output_dir)
