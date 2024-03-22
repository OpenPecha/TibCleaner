from pathlib import Path
from typing import List

from tibcleaner.checkpoint import load_checkpoints
from tibcleaner.docx_to_txt import docx_to_txt
from tibcleaner.epub_to_txt import epub_to_txt
from tibcleaner.html_to_txt import html_to_txt_file
from tibcleaner.img_to_jpeg import convert_image_format_to_jpeg
from tibcleaner.pdf_to_txt_and_jpeg import process_pdf
from tibcleaner.rtf_to_txt import rtf_file_to_txt
from tibcleaner.TXT_to_txt import convert_TXT_to_txt, read_txt_file


def test_epub_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/epub_to_txt")
    epub_files = list(folder_dir.rglob("*.epub"))
    for epub_file in epub_files:
        epub_to_txt(epub_file, output_dir)
        output_file = output_dir / f"{epub_file.stem}.txt"
        output_text = read_txt_file(output_file)
        expected_output_text = read_txt_file(
            output_dir / f"expected_{epub_file.stem}.txt"
        )
        assert (output_dir / f"{epub_file.stem}.txt").exists()
        assert output_text == expected_output_text
        output_file.unlink()


def test_html_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/html_to_txt")
    html_files = list(folder_dir.rglob("*.html"))
    for html_file in html_files:
        html_to_txt_file(html_file, output_dir)
        output_file = output_dir / f"{html_file.stem}.txt"
        output_text = read_txt_file(output_dir / f"{html_file.stem}.txt")
        expected_output_text = read_txt_file(
            output_dir / f"expected_{html_file.stem}.txt"
        )
        assert (output_dir / f"{html_file.stem}.txt").exists()
        assert output_text == expected_output_text
        output_file.unlink()


def test_rtf_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/rtf_to_txt")
    rtf_files = list(folder_dir.rglob("*.rtf"))
    for rtf_file in rtf_files:
        rtf_file_to_txt(rtf_file, output_dir)
        output_file = output_dir / f"{rtf_file.stem}.txt"
        assert (output_dir / f"{rtf_file.stem}.txt").exists()
        output_text = read_txt_file(output_dir / f"{rtf_file.stem}.txt")
        expected_output_text = read_txt_file(
            output_dir / f"expected_{rtf_file.stem}.txt"
        )
        assert output_text == expected_output_text
        output_file.unlink()


def test_docx_to_text():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/docx_to_txt")
    docx_files = list(folder_dir.rglob("*.docx"))
    for docx_file in docx_files:
        docx_to_txt(docx_file, output_dir)
        output_file = output_dir / f"{docx_file.stem}.txt"
        assert (output_dir / f"{docx_file.stem}.txt").exists()
        output_text = read_txt_file(output_dir / f"{docx_file.stem}.txt")
        expected_output_text = read_txt_file(
            output_dir / f"expected_{docx_file.stem}.txt"
        )
        assert output_text == expected_output_text
        output_file.unlink()


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
        output_file_txt = output_dir_txt / f"{pdf_file.stem}.txt"
        output_file_img = output_dir_jpeg / f"{pdf_file.stem}_images"
        if output_file_txt.exists():
            output_file_txt.unlink()
        if output_file_img.exists():
            for img_file in output_file_img.rglob("*"):
                img_file.unlink()
            output_file_img.rmdir()


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
        (output_dir / file_type / f"{img_file.stem}.jpeg").unlink()


def test_TXT_to_txt():
    folder_dir = Path("tests/test_data/ALL_FILES/")
    output_dir = Path("tests/test_data/TXT_to_txt")
    txt_files = list(folder_dir.rglob("*.TXT"))
    for txt_file in txt_files:
        convert_TXT_to_txt(txt_file, output_dir)
        assert (output_dir / f"{txt_file.stem}.txt").exists()
        output_text = read_txt_file(output_dir / f"{txt_file.stem}.txt")
        expected_output_text = read_txt_file(
            output_dir / f"expected_{txt_file.stem}.txt"
        )
        assert output_text == expected_output_text
        (output_dir / f"{txt_file.stem}.txt").unlink()
