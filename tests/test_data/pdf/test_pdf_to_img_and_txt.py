from pathlib import Path

from tibcleaner.checkpoint import load_checkpoints
from tibcleaner.pdf_to_txt_and_jpeg import process_pdf


def test_pdf_to_txt_and_jpeg():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir_txt = Path("tests/test_data/pdf/pdf_to_txt")
    output_dir_jpeg = Path("tests/test_data/pdf/pdf_to_jpeg")
    pdf_files = list(folder_dir.rglob("*.pdf"))
    checkpoints = load_checkpoints()
    for pdf_file in pdf_files:
        process_pdf((pdf_file, output_dir_txt, output_dir_jpeg, checkpoints))
        assert (output_dir_txt / f"{pdf_file.stem}.txt").exists() or (
            output_dir_jpeg / f"{pdf_file.stem}_images"
        ).exists()
        output_file_txt = output_dir_txt / f"{pdf_file.stem}.txt"
        output_file_img = output_dir_jpeg / f"{pdf_file.stem}_images"
        if output_file_txt.exists():
            output_file_txt.unlink()
        if output_file_img.exists():
            for img_file in output_file_img.rglob("*"):
                img_file.unlink()
            output_file_img.rmdir()
