
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort


ROOT = Path(__file__).resolve().parents[2]

VIDEO_PATH = Path(r"C:\Users\hp\Downloads\Manhattan.mp4")

MODELS = [
    ROOT / "models" / "yolo11n.onnx",
    ROOT / "models" / "yolo11n_int8.onnx",
    ROOT / "models" / "yolo11n_int8_v2.onnx",
]

IMAGE_SIZE = 640


def letterbox(image, size=640):
    height, width = image.shape[:2]

    ratio = min(size / height, size / width)

    new_width = round(width * ratio)
    new_height = round(height * ratio)

    resized = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR,
    )

    pad_width = size - new_width
    pad_height = size - new_height

    left = round(pad_width / 2 - 0.1)
    right = round(pad_width / 2 + 0.1)
    top = round(pad_height / 2 - 0.1)
    bottom = round(pad_height / 2 + 0.1)

    padded = cv2.copyMakeBorder(
        resized,
        top,
        bottom,
        left,
        right,
        cv2.BORDER_CONSTANT,
        value=(114, 114, 114),
    )

    rgb = cv2.cvtColor(padded, cv2.COLOR_BGR2RGB)
    tensor = rgb.astype(np.float32) / 255.0
    tensor = np.transpose(tensor, (2, 0, 1))
    tensor = np.expand_dims(tensor, axis=0)

    return np.ascontiguousarray(tensor)


def main():
    cap = cv2.VideoCapture(str(VIDEO_PATH))

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {VIDEO_PATH}")

    success, frame = cap.read()
    cap.release()

    if not success:
        raise RuntimeError("Cannot read the first video frame.")

    input_tensor = letterbox(frame, IMAGE_SIZE)

    for model_path in MODELS:
        if not model_path.exists():
            print(f"\nModel not found: {model_path}")
            continue

        session = ort.InferenceSession(
            str(model_path),
            providers=["CPUExecutionProvider"],
        )

        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name

        output = session.run(
            [output_name],
            {input_name: input_tensor},
        )[0]

        class_scores = output[:, 4:, :]

        print(f"\nModel: {model_path.name}")
        print("Output shape:", output.shape)
        print("Minimum:", float(output.min()))
        print("Maximum:", float(output.max()))
        print("Mean:", float(output.mean()))
        print("Maximum class score:", float(class_scores.max()))
        print("Nonzero class scores:", int(np.count_nonzero(class_scores)))


if __name__ == "__main__":
    main()
