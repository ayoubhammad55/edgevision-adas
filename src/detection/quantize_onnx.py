
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
import onnx

from onnxruntime.quantization import (
    CalibrationDataReader,
    QuantFormat,
    QuantType,
    quantize_static,
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

VIDEO_PATH = Path(r"C:\Users\hp\Downloads\Manhattan.mp4")

MODEL_PATH = ROOT / "models" / "yolo11n.onnx"
OUTPUT_PATH = ROOT / "models" / "yolo11n_int8_v2.onnx"

IMAGE_SIZE = 640
CALIBRATION_FRAMES = 100


# --------------------------------------------------
# YOLO Letterbox Preprocessing
# --------------------------------------------------

def letterbox(image, new_shape=640, color=(114, 114, 114)):
    """
    Resize an image while preserving its aspect ratio.
    Add padding to obtain the target dimensions.
    """

    height, width = image.shape[:2]

    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    ratio = min(
        new_shape[0] / height,
        new_shape[1] / width,
    )

    new_width = int(round(width * ratio))
    new_height = int(round(height * ratio))

    resized = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR,
    )

    padding_width = new_shape[1] - new_width
    padding_height = new_shape[0] - new_height

    left = int(round(padding_width / 2 - 0.1))
    right = int(round(padding_width / 2 + 0.1))

    top = int(round(padding_height / 2 - 0.1))
    bottom = int(round(padding_height / 2 + 0.1))

    padded = cv2.copyMakeBorder(
        resized,
        top,
        bottom,
        left,
        right,
        cv2.BORDER_CONSTANT,
        value=color,
    )

    return padded


# --------------------------------------------------
# Calibration Data Reader
# --------------------------------------------------

class VideoCalibrationReader(CalibrationDataReader):

    def __init__(self, video_path, input_name, max_frames=100):

        self.video_path = str(video_path)
        self.input_name = input_name
        self.max_frames = max_frames

        self.cap = None
        self.frames_read = 0

        self.rewind()

    def rewind(self):

        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(self.video_path)
        self.frames_read = 0

    def get_next(self):

        if self.frames_read >= self.max_frames:
            return None

        success, frame = self.cap.read()

        if not success:
            return None

        # Preserve aspect ratio using YOLO-style letterboxing.
        image = letterbox(frame, IMAGE_SIZE)

        # BGR -> RGB.
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        # Normalize to [0, 1].
        image = image.astype(np.float32) / 255.0

        # HWC -> CHW.
        image = np.transpose(image, (2, 0, 1))

        # Add batch dimension.
        image = np.expand_dims(image, axis=0)

        self.frames_read += 1

        if self.frames_read % 10 == 0:
            print(
                f"Calibration frames prepared: "
                f"{self.frames_read}/{self.max_frames}"
            )

        return {
            self.input_name: image
        }

    def __del__(self):

        if self.cap is not None:
            self.cap.release()


# --------------------------------------------------
# Main Quantization Function
# --------------------------------------------------

def main():

    if not VIDEO_PATH.exists():
        raise FileNotFoundError(
            f"Video not found: {VIDEO_PATH}"
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"ONNX model not found: {MODEL_PATH}"
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Load the original ONNX model.
    session = ort.InferenceSession(
        str(MODEL_PATH),
        providers=["CPUExecutionProvider"],
    )

    input_name = session.get_inputs()[0].name

    print("Input name:", input_name)
    print("Input shape:", session.get_inputs()[0].shape)

    del session

    # Prepare calibration data.
    reader = VideoCalibrationReader(
        VIDEO_PATH,
        input_name,
        CALIBRATION_FRAMES,
    )

    # Identify the final six Conv nodes.
    # These are the detection-head output convolutions
    # in the standard exported YOLO11n graph.
    onnx_model = onnx.load(str(MODEL_PATH))

    conv_nodes = [
        node
        for node in onnx_model.graph.node
        if node.op_type == "Conv"
    ]

    if len(conv_nodes) < 6:
        raise RuntimeError(
            "Unexpected ONNX graph: fewer than six Conv nodes."
        )

    excluded_nodes = conv_nodes[-6:]

    nodes_to_exclude = [
        node.name
        for node in excluded_nodes
    ]

    if any(not name for name in nodes_to_exclude):
        raise RuntimeError(
            "One or more excluded Conv nodes have no name."
        )

    print("\nConvolution operators:", len(conv_nodes))
    print("Excluded detection-head operators:")

    for node_name in nodes_to_exclude:
        print(" -", node_name)

    print("\nStarting static INT8 quantization...")
    print("Input model:", MODEL_PATH)
    print("Output model:", OUTPUT_PATH)

    try:

        quantize_static(
            model_input=str(MODEL_PATH),
            model_output=str(OUTPUT_PATH),
            calibration_data_reader=reader,

            quant_format=QuantFormat.QDQ,

            activation_type=QuantType.QUInt8,
            weight_type=QuantType.QInt8,

            per_channel=True,

            op_types_to_quantize=[
                "Conv",
                "MatMul",
                "Gemm",
            ],

            nodes_to_exclude=nodes_to_exclude,
        )

    finally:

        if reader.cap is not None:
            reader.cap.release()

    print("\nQuantization completed.")

    print("INT8 model:", OUTPUT_PATH)

    print(
        "Model size:",
        f"{OUTPUT_PATH.stat().st_size / (1024 * 1024):.2f} MB",
    )


if __name__ == "__main__":
    main()
