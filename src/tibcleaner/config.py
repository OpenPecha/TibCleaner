from pathlib import Path


def _mkdir(path):
    if path.is_dir():
        return path
    path.mkdir(exist_ok=True, parents=True)
    return path


CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent.parent
DATA_DIR = _mkdir(ROOT_DIR / "DATA")

BASE_PATH = Path.home()
DOC_CONVERT_CHECKPOINT_FILE = BASE_PATH / "doc_to_docx_checkpoint.txt"
DOCX_CONVERT_CHECKPOINT_FILE = BASE_PATH / "docx_to_txt_checkpoint.txt"


def load_doc_checkpoints():
    if DOC_CONVERT_CHECKPOINT_FILE.exists():
        return DOC_CONVERT_CHECKPOINT_FILE.read_text().splitlines()

    DOC_CONVERT_CHECKPOINT_FILE.touch()
    return []


def save_doc_checkpoint(file_checkpoint):
    with open(DOC_CONVERT_CHECKPOINT_FILE, "a") as f:
        f.write(f"{file_checkpoint}\n")


def load_docx_checkpoints():
    if DOCX_CONVERT_CHECKPOINT_FILE.exists():
        return DOCX_CONVERT_CHECKPOINT_FILE.read_text().splitlines()

    DOCX_CONVERT_CHECKPOINT_FILE.touch()
    return []


def save_docx_checkpoint(file_checkpoint):
    with open(DOCX_CONVERT_CHECKPOINT_FILE, "a") as f:
        f.write(f"{file_checkpoint}\n")
