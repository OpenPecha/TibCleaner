from pathlib import Path

from tibcleaner.zip_rename_unzip import extract_zip_files as zip_renanme_extract
from tibcleaner.zip_to_unzip import extract_rar_files, extract_zip_files


def test_zip_rename_extract():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/zip_rename_extract")
    zip_files = list(folder_dir.rglob("*.zip"))
    zip_renanme_extract(zip_files, output_dir, "A")
    assert (output_dir).exists()
    assert (output_dir / "A_filename_mapping.csv").exists()
    csv_file = output_dir / "A_filename_mapping.csv"
    expected_csv_file = Path(f"{output_dir}/expected_A_filename_mapping.csv")
    assert csv_file.read_text() == expected_csv_file.read_text()


def test_zip_extract():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/zip_extract")
    zip_files = list(folder_dir.rglob("*.zip"))
    extract_zip_files(zip_files, output_dir)
    for zip_file in zip_files:
        assert (output_dir / f"{zip_file.stem}").exists()


def test_rar_extract():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/rar_extract")
    rar_files = list(folder_dir.rglob("*.rar"))
    extract_rar_files(rar_files, output_dir)
    for rar_file in rar_files:
        assert (output_dir / f"{rar_file.stem}").exists()
