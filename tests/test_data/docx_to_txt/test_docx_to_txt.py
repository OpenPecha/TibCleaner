from pathlib import Path

from tibcleaner.docx_to_txt import docx_to_txt


def test_docx_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/docx_to_txt")
    docx_files = list(folder_dir.rglob("*.docx"))
    for docx_file in docx_files:
        docx_to_txt(docx_file, output_dir)
        assert (output_dir / f"{docx_file.stem}.txt").exists()
        (output_dir / f"{docx_file.stem}.txt").unlink()
