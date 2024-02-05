import subprocess
from pathlib import Path

from tibcleaner.config import DATA_DIR


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


if __name__ == "__main__":
    doc_path = DATA_DIR / "《རྦ་བཞེད་》ཕྱོགས་བསྒྲིགས།.doc"
    convert_doc_to_docx(doc_path, destination_dir=DATA_DIR)
