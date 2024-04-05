from pathlib import Path

from tibcleaner.epub_to_txt import epub_to_txt


def test_epub_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/epub_to_txt")
    epub_files = list(folder_dir.rglob("*.epub"))
    for epub_file in epub_files:
        epub_to_txt(epub_file, output_dir)
        assert (output_dir / f"{epub_file.stem}.txt").exists()
        (output_dir / f"{epub_file.stem}.txt").unlink()
