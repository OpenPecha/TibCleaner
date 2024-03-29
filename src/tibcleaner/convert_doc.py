import logging
import subprocess
from pathlib import Path

from tibcleaner.config import DATA_DIR, load_doc_checkpoints, save_doc_checkpoint
from tibcleaner.filter import get_all_doc_files

log_fn = "doc_to_docx_errors.log"
error_file_log_fn = "docx_to_docx_error_files.log"

logging.basicConfig(
    filename=str(log_fn),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_error_with_id(file_: str):
    """Log error message with ID to a separate file."""
    with open(error_file_log_fn, "a") as log_file:
        log_file.write(f"{file_}\n")


def get_libreoffice_path():
    try:
        result = subprocess.run(
            ["which", "libreoffice"], capture_output=True, check=True, text=True
        )
        if result.stdout:
            return result.stdout.strip()
        else:
            raise RuntimeError("LibreOffice not found")
    except Exception as e:
        raise RuntimeError(f"An error occurred while trying to find LibreOffice: {e}")


def convert_doc_to_docx(doc_file_path: Path, destination_dir: Path):
    libra_office_path = get_libreoffice_path()
    try:
        cmd = [
            libra_office_path,
            "--convert-to",
            "docx",
            "--outdir",
            str(destination_dir),
            str(doc_file_path),
        ]
        result = subprocess.run(cmd, capture_output=True, check=True, text=True)
        if result.stderr:
            raise RuntimeError(f"Error occured on Converting file {doc_file_path.name}")
    except Exception as e:
        raise RuntimeError(
            f"Error occured on Converting file {doc_file_path.name}: {e}"
        )


def covert_doc_files_pipeline(folder_dir: Path, destination_dir: Path):
    files = get_all_doc_files(folder_dir)
    doc_checkpoints = load_doc_checkpoints()
    for file in files:
        if file not in doc_checkpoints:
            try:
                convert_doc_to_docx(file, destination_dir)
                save_doc_checkpoint(file)
            except Exception as e:
                logging.error(f"An error occurred while converting {file.name}: {e}")
                log_error_with_id(file)
                continue


if __name__ == "__main__":
    covert_doc_files_pipeline(DATA_DIR, destination_dir=DATA_DIR)
