from multiprocessing import Pool
from pathlib import Path
from typing import List

from tqdm import tqdm

from tibcleaner.checkpoint import load_checkpoints
from tibcleaner.docx_to_txt import docx_to_txt
from tibcleaner.epub_to_txt import epub_to_txt
from tibcleaner.html_to_txt import html_to_txt
from tibcleaner.img_to_jpeg import image_to_jpeg
from tibcleaner.pdf_to_txt_and_jpeg import process_pdf
from tibcleaner.rtf_to_txt import rtf_to_txt
from tibcleaner.TXT_to_txt import TXT_to_txt


def worker_task(args):
    file, output_dir, checkpoints = args
    file = Path(file)
    if f"{str(file)}" in checkpoints:
        return
    # Pass the type-specific output directory to conversion functions
    if file.suffix.lower() in [".html", ".htm"]:
        html_to_txt(file, output_dir / file.suffix[1:])
    elif file.suffix.lower() == ".rtf":
        rtf_to_txt(file, output_dir / file.suffix[1:])
    elif file.suffix.lower() == ".epub":
        epub_to_txt(file, output_dir / file.suffix[1:])
    elif file.suffix.lower() == ".docx":
        docx_to_txt(file, output_dir / file.suffix[1:])
    elif file.suffix.lower() == ".pdf":
        process_pdf(
            (
                file,
                output_dir / file.suffix[1:] / "txt",
                output_dir / file.suffix[1:] / "img",
                checkpoints,
            )
        )
    elif file.suffix.lower() in [
        ".png",
        ".pcx",
        ".jpg",
        ".gif",
        ".tif",
        ".svg",
        ".bmp",
        ".jpeg",
    ]:
        image_to_jpeg(file, output_dir / "img")
    elif file.suffix == ".TXT":
        TXT_to_txt(file, output_dir / file.suffix[1:])
    else:
        print(f"[WARNING] Unsupported file type: {file.suffix}, File: {file}")


# Note: Updated the 'elif' for PDF to TXT and JPEG conversion to fit the expected arguments structure of `process_pdf`.
# Ensure the `process_pdf` function is adapted to handle the directory paths correctly, especially if it expects
# specific subdirectories for images and text.


def files_to_txt(all_files: List[Path], output_dir: Path, num_processes: int = 10):
    checkpoints = load_checkpoints()
    tasks = [(file, output_dir, checkpoints) for file in all_files]

    num_processes = num_processes
    with Pool(processes=num_processes) as pool:
        list(
            tqdm(
                pool.imap(worker_task, tasks),
                total=len(tasks),
                desc="Converting files to txt",
            )
        )


if __name__ == "__main__":
    folder_dir = Path(
        "/home/gangagyatso/Desktop/work/TibCleaner/tests/test_data/ALL_FILES"
    )
    all_files = list(folder_dir.rglob("*"))
    output_dir = Path("/home/gangagyatso/Desktop/work/TibCleaner/data/")
    num_processes = 10
    files_to_txt(all_files, output_dir, num_processes)
