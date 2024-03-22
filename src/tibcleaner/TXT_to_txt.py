# importing libraries
from pathlib import Path

from tqdm import tqdm

from tibcleaner.checkpoint import (
    load_checkpoints,
    save_checkpoint,
    save_corrupted_files,
)
from tibcleaner.utils import _mkdir


def read_txt_file(txt_file_path: Path) -> str:
    """Reads the content of a TXT file"""
    with open(txt_file_path, encoding="utf-8") as txt_file:
        text = txt_file.read()
        return text


def convert_TXT_to_txt(file_path: Path, output_dir: Path):
    text = ""
    try:
        output_dir = _mkdir(output_dir)
        text = read_txt_file(file_path)

        output_file = output_dir / f"{file_path.stem}.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)
        save_checkpoint(file_path)
        return output_file
    except Exception as e:
        save_corrupted_files(file_path, str(e))
        return None


if __name__ == "__main__":
    output_dir = Path("txt/A")
    _mkdir(output_dir)
    all_TXT_files = list(Path("txt/A").glob("*.TXT"))
    checkpoints = load_checkpoints()
    for TXT_file in tqdm(all_TXT_files, desc="Converting TXT to txt"):
        if str(TXT_file) in checkpoints:
            continue
        convert_TXT_to_txt(TXT_file, output_dir)
    print("Finished converting all TXT files to txt")
