from multiprocessing import Pool
from pathlib import Path
from typing import List

from tqdm import tqdm

from tibcleaner.checkpoint import load_checkpoints


def file_extn_to_txt(file: Path, output_dir: Path):
    pass


def worker_task(args):
    file, output_dir, checkpoints = args
    if f"{str(file)}" in checkpoints:
        return
    file_extn_to_txt(file, output_dir)


def convert_rtf_files_to_txt(all_files: List[Path], output_dir: Path):
    checkpoints = load_checkpoints()
    tasks = [(file, output_dir, checkpoints) for file in all_files]

    num_processes = 10
    with Pool(processes=num_processes) as pool:
        list(
            tqdm(
                pool.imap(worker_task, tasks),
                total=len(tasks),
                desc="Converting PDF files to txt",
            )
        )


if __name__ == "__main__":
    folder_dir = Path("root/A")
    dir_name = "A"
    all_files = list(folder_dir.rglob("*.file_type"))
    output_dir = Path("output/A")
    convert_rtf_files_to_txt(all_files, output_dir)
