# Importing files
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm

from tibcleaner.checkpoint import (
    load_checkpoints,
    save_checkpoint,
    save_corrupted_files,
)
from tibcleaner.utils import _mkdir

"""function to convert html to txt file"""


def html_to_txt(file_path: Path, output_dir: Path):
    _mkdir(output_dir)
    output_file = output_dir / f"{file_path.stem}.txt"
    text = ""
    if file_path.suffix.lower() in [".html", ".htm"]:
        text = read_html_file(file_path)
        if text:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(text)
            save_checkpoint(file_path)
            return output_file


def read_html_file(html_file_path: Path) -> str:
    """Reads the content of an HTML file"""
    try:
        with open(html_file_path, encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")
            text = soup.get_text()
            return text
    except Exception as e:
        print(f"html file {html_file_path} is corrupted")
        save_corrupted_files(html_file_path, f"Error processing {html_file_path}: {e}")
        return ""


if __name__ == "__main__":
    output_dir = Path("/root/html_to_txt/A/")
    html_files = list(Path("/root/A/").rglob("*.html"))
    html_files.extend(list(Path("/root/A/").rglob("*.htm")))
    checkpoints = load_checkpoints()
    for html_file in tqdm(html_files, desc="Converting HTML to txt"):
        if str(html_file) in checkpoints:
            continue
        html_to_txt(html_file, output_dir)
