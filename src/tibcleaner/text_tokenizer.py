import os
import re
from multiprocessing import Pool
from pathlib import Path
from typing import List

import botok
from tqdm import tqdm

from tibcleaner.checkpoint import (
    load_checkpoints,
    save_checkpoint,
    save_corrupted_files,
)

SENT_PER_LINE_STR = str  # sentence per line string
bo_word_tokenizer = None


def get_bo_word_tokenizer():
    global bo_word_tokenizer
    if bo_word_tokenizer is None:
        bo_word_tokenizer = botok.WordTokenizer()
    return bo_word_tokenizer


def bo_preprocess(text: str) -> str:
    text = text.replace("\r", "").replace("\n", "")
    return text


def bo_sent_tokenizer(text: str) -> SENT_PER_LINE_STR:
    """Tokenize a text into sentences."""
    print("[INFO] Tokenizing Tibetan text...")

    def get_token_text(token):
        if hasattr(token, "text_cleaned") and token.text_cleaned:
            return token.text_cleaned
        else:
            return token.text

    # fmt: off
    opening_puncts = ['༁', '༂', '༃', '༄', '༅', '༆', '༇', '༈', '༉', '༊', '༑', '༒', '༺', '༼', '༿', '࿐', '࿑', '࿓', '࿔', '࿙']  # noqa: E501
    closing_puncts = ['།', '༎', '༏', '༐', '༔', '༴', '༻', '༽', '༾', '࿚']  # noqa: E501
    skip_chunk_types = [botok.vars.CharMarkers.CJK.name, botok.vars.CharMarkers.LATIN.name, botok.vars.CharMarkers.OTHER.name]  # noqa: E501
    # fmt: on

    # Regex to improve the chunking of shunits, this will be replaced by a better sentence segmentation in botok
    r_replace = [
        (r"༼༼[༠-༩]+[བན]༽", r""),  # delete source image numbers `ས་༼༤བ༽མེད་བ`
        (
            r"([^ང])་([༔།])",
            r"\1\2",
        ),  # delete spurious spaces added by botok in the cleantext values
        (
            r"([།གཤ]{1,2})\s+(།{1,2})",
            r"\1\2 ",
        ),  # Samdong Rinpoche style double shad. This needs to be applied on inference input
        # (r"", r""),
    ]

    text = bo_preprocess(text)
    sents_words = []
    tokenizer = get_bo_word_tokenizer()
    tokens = tokenizer.tokenize(text, split_affixes=False)
    for token in tokens:
        if token.chunk_type in skip_chunk_types:
            continue
        token_text = get_token_text(token)
        if any(punct in token_text for punct in opening_puncts):
            sents_words.append(token_text.strip())
        elif any(punct in token_text for punct in closing_puncts):
            sents_words.append(token_text.strip())
            sents_words.append("\n")
        else:
            sents_words.append(token_text)

    sents_text = "".join(sents_words)

    for fr, to in r_replace:
        sents_text = re.sub(fr, to, sents_text)

    return sents_text


def process_text(args):
    txt_file, output_dir, checkpoints = args
    try:
        if f"{str(txt_file)}" in checkpoints:
            return
        with open(txt_file, encoding="utf-8") as f:
            text = f.read()

        tokenized_text = bo_sent_tokenizer(text)

        # Define the output file path
        output_file_path = os.path.join(output_dir, os.path.basename(txt_file))

        # Save the tokenized text to a new file
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(tokenized_text)

        print(f"Processed and saved tokenized text to {output_file_path}")
        save_checkpoint(txt_file)

    except Exception as e:
        print(f"[ERROR] Processing failed for {txt_file}: {e}")
        save_corrupted_files(txt_file, str(e))


def all_file_text_tokenize(txt_files: List[Path], output_dir: Path):
    checkpoints = load_checkpoints()
    tasks = [(txt_file, output_dir, checkpoints) for txt_file in txt_files]

    num_processes = 20  # Adjust based on your system capabilities

    # Use a Pool to manage multiple processes
    with Pool(processes=num_processes) as pool:
        # Note: tqdm might not directly work with pool.map or pool.starmap in Jupyter notebooks without some tweaks
        list(
            tqdm(
                pool.imap(process_text, tasks), total=len(tasks), desc="tokenizing text"
            )
        )
    print("Finished tokenizing text")


if __name__ == "__main__":
    # Define the input directory
    input_dir = Path("path/to/input/dir")

    # Define the output directory
    output_dir = Path("path/to/output/dir")

    # Get a list of all files in the input directory
    txt_files = list(input_dir.glob("*.txt"))

    # Tokenize all files and save the tokenized text to the output directory
    all_file_text_tokenize(txt_files, output_dir)
