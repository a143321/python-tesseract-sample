"""
text_utils.py:
Utilities for handling and processing text data.
"""

import os
import difflib
from colorama import init, Fore


def get_diff(actual_text: str, expected_text: str) -> list:

    init(autoreset=True)

    diff = difflib.Differ()
    output_diff = list(diff.compare(actual_text.splitlines(), expected_text.splitlines()))

    for line in output_diff:
        if line.startswith('+ '):
            # 追加された行を緑色で表示
            print(Fore.GREEN + line)
        elif line.startswith('- '):
            # 削除された行を赤色で表示
            print(Fore.RED + line)
        else:
            print(line)

    return output_diff


def remove_unnecessary_newlines(text: str) -> str:
    """
    半角スペースを除く文字列のある有効な行のみ抽出する

    Args:
    - text (str): target text

    Returns:
    - str: cleaned text
    """

    # 連続した改行を一つに置換
    cleaned_text = os.linesep.join([line for line in text.splitlines() if line.strip()])
    return cleaned_text


def get_result_from_text_file(file_path: str) -> str:
    """
    Read the content of a given text file.

    Args:
    - file_path (str): Path to the text file.

    Returns:
    - str: Content of the text file.
    """

    # エラーハンドリングの追加
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content


def count_characters(text: str, ignore_spaces: bool = False) -> int:
    """
    Count characters in the given text. Optionally ignoring spaces.

    Args:
    - text (str): Text to count characters from.
    - ignore_spaces (bool): If True, ignores both full-width and half-width spaces.

    Returns:
    - int: Number of characters.
    """

    # 改行文字を取り除く
    cleaned_text = text.replace(os.linesep, '')

    if ignore_spaces:
        # 全角・半角スペースを取り除く
        cleaned_text = cleaned_text.replace(' ', '').replace('　', '')

    return len(cleaned_text)
