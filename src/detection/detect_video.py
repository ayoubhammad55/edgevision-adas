
import argparse
import csv
import statistics
import time
from pathlib import Path

import cv2
import psutil
from ultralytics import YOLO


# Project paths
ROOT = Path(__file__).resolve().parents[2]

DEFAULT_MODEL = ROOT / "models" / "yolo11n.pt"
DEFAULT_VIDEO = Path.home() / "Downloads" / "Manhattan.mp4"
DEFAULT_OUTPUT = ROOT / "results" / "detection" / "manhattan_yolo11n.mp4"
DEFAULT_CSV = ROOT / "results" / "detection" / "detection_benchmark.csv"


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLO11n video object detection benchmark"
    )

    parser.add_argument("--video", type=Path, default=DEFAULT_VIDEO)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-frames", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--device", default="cpu")

    return parser.parse_args()


def percentile(values, percentage):
    if not values:
        return 0.0

    return statistics.quantiles(
        values, n=100
    )[percentage - 1] if len(values) >= 100 else sorted(values)[
        min(len(values) - 1, round((percentage / 100) * (len(values) - 1)))
    ]


def main():
    args = parse_args()

    if not args.video.exists():
        raise FileNotFoundError(f"Video not found: {args.video}")

    if not args.model.exists():
        raise FileNotFoundError(f"Model not found: {args.model}")

    print("=" * 55)
    print("EDGEVISION - YOLO11n OBJECT DETECTION")
    print("=" * 55)

    print(f"Video: {args.video}")
    print(f"Model: {args.model}")
    print(f"Device: {args.device}")
    print(f"Image size: {args.imgsz}")
    print(f"Maximum frames: {args.max_frames}")

    # Load model
    print("\nLoading YOLO model...")
    model = YOLO(str(args.model))
    print("Model loaded successfully.")

    # Open video
    cap = cv2.VideoCapture(str(args.video))

    if not cap.isOpened():
        raise RuntimeError("Could not open video.")

    total_metadata_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    source_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"\nVideo resolution: {width}x{height}")
    print(f"Source FPS: {source_fps:.2f}")
    print(f"Metadata frames: {total_metadata_frames}")

    ret, first_frame = cap.read()

    if not ret:
        cap.release()
        raise RuntimeError("Could not read the first video frame.")

    # Warm-up inference (excluded from benchmark measurements)
    print("\nWarming up model...")
    model.predict(
        first_frame,
        imgsz=args.imgsz,
        conf=args.conf,
        device=args.device,
        verbose=False
    )
    print("Warm-up complete.")

    # Prepare output
    args.output.parent.mkdir(parents=True, exist_ok=True)

    output_fps = source_fps if source_fps > 0 else 30.0

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        str(args.output),
        fourcc,
        output_fps,
        (width, height)
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not create output video.")

    inference_times = []
    processed_frames = 0
    process = psutil.Process()

    # Process video
    print("\nStarting detection...\n")

    start_time = time.perf_counter()
    next_frame = first_frame

    try:
        while True:
            if args.max_frames > 0 and processed_frames >= args.max_frames:
                break

            if next_frame is None:
                ret, frame = cap.read()

                if not ret:
                    break
            else:
                frame = next_frame
                next_frame = None

            # Measure model inference
            inference_start = time.perf_counter()

            results = model.predict(
                frame,
                imgsz=args.imgsz,
                conf=args.conf,
                device=args.device,
                verbose=False
            )

            inference_end = time.perf_counter()

            inference_times.append(
                (inference_end - inference_start) * 1000
            )

            # Draw detections
            annotated_frame = results[0].plot()

            # Save annotated frame
            writer.write(annotated_frame)

            processed_frames += 1

            # Progress
            if processed_frames % 25 == 0:
                elapsed = time.perf_counter() - start_time
                current_fps = processed_frames / elapsed

                detections = len(results[0].boxes)

                print(
                    f"Processed: {processed_frames} frames | "
                    f"FPS: {current_fps:.2f} | "
                    f"Detections: {detections}"
                )

    finally:
        total_time = time.perf_counter() - start_time
        cap.release()
        writer.release()

    # Calculate metrics
    if processed_frames == 0:
        raise RuntimeError("No frames were processed.")

    inference_seconds = sum(inference_times) / 1000

    inference_fps = (
        processed_frames / inference_seconds
        if inference_seconds > 0 else 0
    )

    pipeline_fps = (
        processed_frames / total_time
        if total_time > 0 else 0
    )

    average_latency = statistics.mean(inference_times)
    median_latency = statistics.median(inference_times)
    p95_latency = percentile(inference_times, 95)

    ram_mb = process.memory_info().rss / (1024 ** 2)

    print("\n" + "=" * 55)
    print("DETECTION BENCHMARK RESULTS")
    print("=" * 55)

    print(f"Processed frames:       {processed_frames}")
    print(f"Total processing time:  {total_time:.2f} seconds")
    print(f"Inference FPS:          {inference_fps:.2f}")
    print(f"Pipeline FPS:           {pipeline_fps:.2f}")
    print(f"Average latency:        {average_latency:.2f} ms")
    print(f"Median latency:         {median_latency:.2f} ms")
    print(f"P95 latency:            {p95_latency:.2f} ms")
    print(f"Process RAM at end:     {ram_mb:.2f} MB")

    print(f"\nAnnotated video: {args.output}")

    # Save benchmark CSV
    args.csv = DEFAULT_CSV
    args.csv.parent.mkdir(parents=True, exist_ok=True)

    file_exists = args.csv.exists()

    with open(args.csv, "a", newline="", encoding="utf-8") as file:
        fields = [
            "model",
            "video",
            "device",
            "image_size",
            "frames",
            "inference_fps",
            "pipeline_fps",
            "average_latency_ms",
            "median_latency_ms",
            "p95_latency_ms",
            "total_time_seconds",
            "process_ram_mb"
        ]

        csv_writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            csv_writer.writeheader()

        csv_writer.writerow({
            "model": args.model.name,
            "video": args.video.name,
            "device": args.device,
            "image_size": args.imgsz,
            "frames": processed_frames,
            "inference_fps": round(inference_fps, 2),
            "pipeline_fps": round(pipeline_fps, 2),
            "average_latency_ms": round(average_latency, 2),
            "median_latency_ms": round(median_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "total_time_seconds": round(total_time, 2),
            "process_ram_mb": round(ram_mb, 2)
        })

    print(f"Benchmark CSV: {args.csv}")
    print("\nBenchmark completed successfully.")


if __name__ == "__main__":
    main()
