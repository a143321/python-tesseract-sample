import os
import difflib

import cv2
import numpy as np
from PIL import Image
import pytesseract

from text_utils import count_characters, remove_unnecessary_newlines, get_result_from_text_file, get_diff


def save_image(img_cv2: np.ndarray, save_image_path: str):
    """
    Save the OpenCV image to the specified path.

    Args:
    - img_cv2 (np.ndarray): Image in OpenCV format to save.
    - save_image_path (str): Path where the image should be saved.
    """
    img_pil = Image.fromarray(cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB))
    img_pil.save(save_image_path)


def ocr_from_image(image_path: str, convert_to_gray=True, apply_binarization=False, lang="jpn+eng", psm=6) -> str:
    """
    Extract text from an image using OCR.

    Args:
    - image_path (str): Path to the input image.
    - convert_to_gray(bool, optional) : Convert image to gray scale.. Default is True.
    - apply_binarization(bool, optional) : Perform binarization. Default is False.
    - lang(str, optional): Select language. Default is "jpn+eng"
    - psm (int, optional): Page segmentation mode for Tesseract OCR. Default is 6.

    Returns:
    - str: Extracted text from the image.
    """

    # When performing binarization, be sure to perform grayscale
    if apply_binarization:
        convert_to_gray = True

    # Convert from Pillow to OpenCV format
    img_pil = np.array(Image.open(image_path))
    img_cv2 = cv2.cvtColor(img_pil, cv2.COLOR_RGB2BGR)

    # Convert to grayscale for noise reduction
    if convert_to_gray:
        img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        save_image(img_cv2, os.path.join(WORK_PATH, "work_gray.png"))

    # Optional binarization
    if apply_binarization:
        _, img_cv2 = cv2.threshold(img_cv2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        save_image(img_cv2, os.path.join(WORK_PATH, "work_binary.png"))

    save_image(img_cv2, os.path.join(WORK_PATH, "work_result.png"))

    # Perform OCR
    # --oem 1 : only use LSTM models
    config = f"--psm {psm} --oem 1 -c preserve_interword_spaces=1"
    return pytesseract.image_to_string(img_cv2, lang=lang, config=config)


if __name__ == "__main__":

    # Set Tesseract path (for Windows)
    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # 作成したいディレクトリのパスを指定
    WORK_PATH = "work_image"

    if not os.path.exists(WORK_PATH):
        os.makedirs(WORK_PATH)

    image_path = "input_images\テキスト\Japanese_text.png"
    expected_text_path = "input_images\テキスト\Japanese_text.txt"
    # image_path = "input_images\テキスト\English_text.png"
    # expected_text_path = "input_images\テキスト\English_text.txt"
    # image_path = "input_images\テキスト\Japanese_text.png"
    # expected_text_path = "input_images\テキスト\Japanese_text.txt"

    actual_text = ocr_from_image(image_path)
    actual_text = remove_unnecessary_newlines(actual_text)
    expected_text = get_result_from_text_file(expected_text_path)
    expected_text = remove_unnecessary_newlines(expected_text)

    print(f"----actual[count : {count_characters(actual_text, True)}]----")
    print(actual_text)
    print(f"----expected[count : {count_characters(expected_text, True)}]----")
    print(expected_text)

    print("----differ----")
    diff = difflib.Differ()
    output_diff = diff.compare(actual_text, expected_text)

    for data in output_diff:

        if data[0:1] in ['+', '-']:
            print(data)

    get_diff(actual_text, expected_text)

    s = difflib.SequenceMatcher(None, actual_text, expected_text)
    print(f"similarity : {difflib.SequenceMatcher(None, actual_text, expected_text).ratio()}")
