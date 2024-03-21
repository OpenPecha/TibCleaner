from pathlib import Path
from typing import List

from tibcleaner.checkpoint import load_checkpoints
from tibcleaner.docx_to_txt import docx_to_txt
from tibcleaner.epub_to_txt import epub_to_txt
from tibcleaner.html_to_txt import html_to_txt_file
from tibcleaner.img_to_jpeg import convert_image_format_to_jpeg
from tibcleaner.pdf_to_txt_and_jpeg import process_pdf
from tibcleaner.rtf_to_txt import rtf_file_to_txt
from tibcleaner.TXT_to_txt import convert_TXT_to_txt
from tibcleaner.zip_rename_unzip import extract_zip_files as zip_renanme_extract
from tibcleaner.zip_to_unzip import extract_rar_files, extract_zip_files


def test_epub_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/epub_to_txt")
    epub_files = list(folder_dir.rglob("*.epub"))
    for epub_file in epub_files:
        epub_to_txt(epub_file, output_dir)
        assert (output_dir / f"{epub_file.stem}.txt").exists()


def test_html_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/html_to_txt")
    html_files = list(folder_dir.rglob("*.html"))
    for html_file in html_files:
        html_to_txt_file(html_file, output_dir)
        assert (output_dir / f"{html_file.stem}.txt").exists()


def test_rtf_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/rtf_to_txt")
    rtf_files = list(folder_dir.rglob("*.rtf"))
    for rtf_file in rtf_files:
        rtf_file_to_txt(rtf_file, output_dir)
        assert (output_dir / f"{rtf_file.stem}.txt").exists()


def test_docx_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/docx_to_txt")
    docx_files = list(folder_dir.rglob("*.docx"))
    for docx_file in docx_files:
        docx_to_txt(docx_file, output_dir)
        assert (output_dir / f"{docx_file.stem}.txt").exists()


def test_pdf_to_txt_and_jpeg():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir_txt = Path("tests/test_data/pdf_to_txt")
    output_dir_jpeg = Path("tests/test_data/pdf_to_jpeg")
    pdf_files = list(folder_dir.rglob("*.pdf"))
    checkpoints = load_checkpoints()
    for pdf_file in pdf_files:
        process_pdf((pdf_file, output_dir_txt, output_dir_jpeg, checkpoints))
        assert (output_dir_txt / f"{pdf_file.stem}.txt").exists() or (
            output_dir_jpeg / f"{pdf_file.stem}_images"
        ).exists()


def test_img_to_jpeg():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/img_to_jpeg")
    """ Filtering the images and then removing the duplicates """
    image_formats = [
        "png",
        "PCX",
        "jpg",
        "JPG",
        "gif",
        "tif",
        "TIF",
        "svg",
        "bmp",
        "BMP",
        "jpeg",
        "JPEG",
    ]
    files: List[Path] = []

    for image_format in image_formats:
        files.extend(folder_dir.rglob(f"*.{image_format}"))

    for img_file in files:
        file_type = img_file.suffix[1:]
        convert_image_format_to_jpeg(img_file, output_dir)
        assert (output_dir / file_type / f"{img_file.stem}.jpeg").exists()


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


def test_TXT_to_txt():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/TXT_to_txt")
    txt_files = list(folder_dir.rglob("*.TXT"))
    for txt_file in txt_files:
        convert_TXT_to_txt(txt_file, output_dir)
        assert (output_dir / f"{txt_file.stem}.txt").exists()


def test_zip_rename_extract():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/zip_rename_extract")
    zip_files = list(folder_dir.rglob("*.zip"))
    zip_renanme_extract(zip_files, output_dir, "A")
    assert (output_dir).exists()
    assert (output_dir / "A_filename_mapping.csv").exists()
