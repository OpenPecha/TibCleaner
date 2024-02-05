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
CHECKPOINT_FILE = BASE_PATH / "doc_to_docx_checkpoint.txt"


def load_doc_checkpoints():
    if CHECKPOINT_FILE.exists():
        return CHECKPOINT_FILE.read_text().splitlines()

    CHECKPOINT_FILE.touch()
    return []


def save_doc_checkpoint(file_checkpoint):
    with open(CHECKPOINT_FILE, "a") as f:
        f.write(f"{file_checkpoint}\n")
