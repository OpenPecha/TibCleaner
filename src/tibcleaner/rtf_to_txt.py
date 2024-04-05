# importing libraries
from pathlib import Path

from striprtf.striprtf import rtf_to_text
from tqdm import tqdm

from tibcleaner.checkpoint import (
    load_checkpoints,
    save_checkpoint,
    save_corrupted_files,
)
from tibcleaner.utils import _mkdir


def rtf_to_txt(file_path: Path, output_dir: Path):
    """Converts a text based file to a txt file"""
    _mkdir(output_dir)
    output_file = output_dir / f"{file_path.stem}.txt"
    text = ""
    file_type = file_path.suffix[1:]

    if file_type in ["rtf", "RTF"]:
        text = read_rtf_file(file_path)
        if text:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(text)
            save_checkpoint(file_path)
            return output_file


def read_rtf_file(file_path: Path) -> str:
    """Reads the content of a RTF file."""
    try:
        with open(file_path, encoding="utf-8") as rtf_file:
            text = rtf_file.read()
            return rtf_to_text(text)
    except Exception as e:
        save_corrupted_files(file_path, str(e))
        return ""


if __name__ == "__main__":
    output_dir = Path("/root/rtf_to_txt/A/")
    files = list(Path("/root/A/").rglob("*.rtf"))
    _mkdir(output_dir)
    checkpoints = load_checkpoints()
    for file in tqdm(files, desc="Converting to txt"):
        if str(file) in checkpoints:
            continue
        rtf_to_txt(file, output_dir)
