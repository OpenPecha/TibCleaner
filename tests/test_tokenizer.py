import os
from pathlib import Path

from tibcleaner.checkpoint import load_checkpoints
from tibcleaner.text_files_tokenizer import all_file_text_tokenize


def test_text_files_tokenizer():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/tokenized_text")
    os.makedirs(output_dir, exist_ok=True)
    txt_files = list(folder_dir.rglob("*.txt"))
    checkpoints = load_checkpoints()
    all_file_text_tokenize(txt_files, output_dir)
    for txt_file in txt_files:
        if f"{str(txt_file)}" in checkpoints:
            assert (output_dir / f"{txt_file.stem}.txt").exists()
            output_text = (output_dir / f"{txt_file.stem}.txt").read_text()
            expected_output_text = (
                output_dir / f"expected_{txt_file.stem}.txt"
            ).read_text()
            assert output_text == expected_output_text
