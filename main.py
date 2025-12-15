import cv2
import numpy as np
import pytesseract
import re
import time
from collections import deque, Counter
import RobotMovement as lm

import RobotMovement

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_for_ocr(frame_bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    bin_img = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel, iterations=1)

    return bin_img


def extract_first_letter(text: str) -> str | None:
    match = re.search(r"[A-Z]", text.upper())
    return match.group(0) if match else None


def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera at index 1")

    last_print_time = 0.0
    print_interval_sec = 0.5

    tesseract_config = r"--oem 3 --psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Keep recent detections
    letter_history = deque(maxlen=30)
    word_history = deque(maxlen=30)
    majority_letter = None
    majority_word = None

    ### FREEZE MODE FLAG
    frozen = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        x1, y1 = int(w * 0.25), int(h * 0.25)
        x2, y2 = int(w * 0.75), int(h * 0.75)
        roi = frame[y1:y2, x1:x2].copy()

        # Always draw ROI (even when frozen)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

        ### -------------------------
        ### FREEZE MODE: Skip OCR
        ### -------------------------
        if frozen:

            # Show the frozen majority letter and wait for key
            if majority_word:
                cv2.putText(frame, f"FINAL: {majority_word}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 3)


            cv2.imshow("Camera", frame)
            cv2.imshow("OCR Binary (ROI)", bin_img)  # show last binary frame

            lm.plot_word(majority_word)

            majority_word = ""

            key = cv2.waitKey(1) & 0xFF

            if key == ord('r'):
                print("Restarting detection...")
                frozen = False
                word_history.clear()
                majority_word = None

            elif key == 27 or key == ord('q'):
                break

            continue  # skip OCR step entirely

        ### -------------------------
        ### NORMAL LIVE OCR
        ### -------------------------

        roi_big = cv2.resize(roi, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        bin_img = preprocess_for_ocr(roi_big)

        ocr_text = pytesseract.image_to_string(bin_img, config=tesseract_config)
        #letter = extract_first_letter(ocr_text)

        if ocr_text:
            word_history.append(ocr_text)
            counts = Counter(word_history)
            majority_word = counts.most_common(1)[0][0]
            #counts = Counter(letter_history)
            #majority_letter = counts.most_common(1)[0][0]

            now = time.time()
            if now - last_print_time > print_interval_sec:
                print(f"Majority Word: {majority_word}")
                last_print_time = now

            ### FREEZE CONDITION:
            ### e.g., majority appears at least 20 times out of last 30
            if word_history.count(majority_word) >= 20:
                print(f"FREEZE: Final word determined → {majority_word}")
                cv2.putText(frame, f"FINAL: {majority_word}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 3)
                frozen = True

        # Display the CURRENT majority (not final)
        if ocr_text and not frozen:
            cv2.putText(frame, f"Detecting: {ocr_text}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 255), 3)

        cv2.imshow("Camera", frame)
        cv2.imshow("OCR Binary (ROI)", bin_img)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


main()
