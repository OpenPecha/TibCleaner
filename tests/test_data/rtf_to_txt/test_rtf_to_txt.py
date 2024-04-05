from pathlib import Path

from tibcleaner.rtf_to_txt import rtf_to_txt


def test_rtf_to_txt():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/TXT_to_txt")
    txt_files = list(folder_dir.rglob("*.rtf")) + list(folder_dir.rglob("*.RTF"))
    for txt_file in txt_files:
        rtf_to_txt(txt_file, output_dir)
        assert (output_dir / f"{txt_file.stem}.txt").exists()
        (output_dir / f"{txt_file.stem}.txt").unlink()
