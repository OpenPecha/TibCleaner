from pathlib import Path

from tibcleaner.html_to_txt import html_to_txt


def test_html_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/html_to_txt")
    html_files = list(folder_dir.rglob("*.html"))
    for html_file in html_files:
        html_to_txt(html_file, output_dir)
        assert (output_dir / f"{html_file.stem}.txt").exists()
        (output_dir / f"{html_file.stem}.txt").unlink()
