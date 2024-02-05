import logging
from pathlib import Path

from docx import Document

from tibcleaner.config import load_docx_checkpoints, save_docx_checkpoint
from tibcleaner.filter import get_all_docx_files

log_fn = "docx_to_txt_errors.log"
error_file_log_fn = "docx_to_txt_error_files.log"

# Configure logging
logging.basicConfig(
    filename=str(log_fn),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_error_with_id(file_: str):
    """Log error message with ID to a separate file."""
    with open(error_file_log_fn, "a") as log_file:
        log_file.write(f"{file_}\n")


def convert_docx_to_txt(docx_file_path: Path, destination_dir: Path):
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
        """load docx file"""
        doc = Document(docx_file_path)
        """extract text and save to txt file"""
        txt_file_path = destination_dir / (docx_file_path.stem + ".txt")
        with txt_file_path.open("w", encoding="utf-8") as txt_file:
            for para in doc.paragraphs:
                txt_file.write(para.text + "\n")
    except Exception as e:
        raise RuntimeError(
            f"Error occurred while converting file {docx_file_path.name}: {e}"
        )


def convert_docx_files_pipeline(folder_dir: Path, destination_dir: Path):
    """
    Convert all DOCX files in a folder to TXT format.
    """
    files = get_all_docx_files(folder_dir)
    doc_checkpoints = load_docx_checkpoints()
    for file in files:
        if file not in doc_checkpoints:
            try:
                convert_docx_to_txt(file, destination_dir)
                save_docx_checkpoint(file)
            except Exception as e:
                logging.error(f"An error occurred while converting {file.name}: {e}")
                log_error_with_id(file)
                continue


if __name__ == "__main__":

    docx_path = Path("data/Doc1.docx")
    output_directory = Path("data")
    txt_path = convert_docx_to_txt(docx_path, output_directory)
    print(f"Converted TXT file saved to: {txt_path}")
