from pathlib import Path

from docx import Document


def convert_docx_to_txt(docx_file_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    """load docx file """
    docx = Document(docx_file_path)
    """extract text from docx file"""
    text = "\n".join(paragraph.text for paragraph in docx.paragraphs)
    txt_file_path = output_dir / (docx_file_path.stem + ".txt")

    with txt_file_path.open("w", encoding="utf-8") as txt_file:
        txt_file.write(text)

    return txt_file_path


if __name__ == "__main__":

    docx_path = Path("data/Doc1.docx")
    output_directory = Path("data")
    txt_path = convert_docx_to_txt(docx_path, output_directory)
    print(f"Converted TXT file saved to: {txt_path}")
