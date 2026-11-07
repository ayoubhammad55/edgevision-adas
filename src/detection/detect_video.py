
import argparse
import csv
import math
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
import psutil
from ultralytics import YOLO


# Project paths
ROOT = Path(__file__).resolve().parents[2]

DEFAULT_MODEL = ROOT / "models" / "yolo11n.pt"
DEFAULT_VIDEO = Path.home() / "Downloads" / "Manhattan.mp4"
DEFAULT_OUTPUT = ROOT / "results" / "detection" / "manhattan_yolo11n.mp4"

# New CSV file to preserve existing benchmark data
DEFAULT_CSV = ROOT / "results" / "detection" / "benchmark_runs.csv"


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLO video object detection benchmark"
    )

    parser.add_argument("--video", type=Path, default=DEFAULT_VIDEO)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--max-frames", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--device", default="cpu")

    args = parser.parse_args()

    if args.max_frames < 0:
        parser.error("--max-frames must be 0 or greater.")

    if args.imgsz <= 0:
        parser.error("--imgsz must be greater than 0.")

    if not 0 < args.conf < 1:
        parser.error("--conf must be between 0 and 1.")

    return args


def percentile(values, percentage):
    """Calculate percentile using the nearest-rank method."""
    if not values:
        return 0.0

    ordered = sorted(values)
    index = max(0, math.ceil(percentage / 100 * len(ordered)) - 1)

    return ordered[index]


def save_benchmark(csv_path, row):
    """Append one benchmark result without overwriting previous runs."""

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "timestamp",
        "model",
        "model_format",
        "video",
        "device",
        "image_size",
        "confidence",
        "max_frames",
        "frames",
        "inference_fps",
        "pipeline_fps",
        "average_latency_ms",
        "median_latency_ms",
        "p95_latency_ms",
        "total_time_seconds",
        "process_ram_mb",
    ]

    file_exists = csv_path.exists() and csv_path.stat().st_size > 0

    if file_exists:
        with open(csv_path, "r", newline="", encoding="utf-8") as file:
            existing_fields = next(csv.reader(file), [])

        if existing_fields != fields:
            raise ValueError(
                f"CSV columns do not match the expected schema: {csv_path}\n"
                "Use a new CSV file or move the old file before continuing."
            )

    with open(csv_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def main():
    args = parse_args()

    if not args.video.exists():
        raise FileNotFoundError(f"Video not found: {args.video}")

    if not args.model.exists():
        raise FileNotFoundError(f"Model not found: {args.model}")

    model_format = args.model.suffix.lower().lstrip(".")
    timestamp = datetime.now(timezone.utc).isoformat()

    print("=" * 55)
    print("EDGEVISION - OBJECT DETECTION BENCHMARK")
    print("=" * 55)

    print(f"Video: {args.video}")
    print(f"Model: {args.model}")
    print(f"Model format: {model_format}")
    print(f"Device: {args.device}")
    print(f"Image size: {args.imgsz}")
    print(f"Confidence: {args.conf}")
    print(f"Maximum frames: {args.max_frames}")
    print(f"CSV output: {args.csv}")

    # Load model
    print("\nLoading model...")
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

    # Warm-up (excluded from benchmark measurements)
    print("\nWarming up model...")

    model.predict(
        first_frame,
        imgsz=args.imgsz,
        conf=args.conf,
        device=args.device,
        verbose=False,
    )

    print("Warm-up complete.")

    # Prepare output video
    args.output.parent.mkdir(parents=True, exist_ok=True)

    output_fps = source_fps if source_fps > 0 else 30.0

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(args.output),
        fourcc,
        output_fps,
        (width, height),
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not create output video.")

    inference_times = []
    processed_frames = 0
    process = psutil.Process()

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

            # Measure model prediction time
            inference_start = time.perf_counter()

            results = model.predict(
                frame,
                imgsz=args.imgsz,
                conf=args.conf,
                device=args.device,
                verbose=False,
            )

            inference_end = time.perf_counter()

            inference_times.append(
                (inference_end - inference_start) * 1000
            )

            # Draw detections and save frame
            annotated_frame = results[0].plot()
            writer.write(annotated_frame)

            processed_frames += 1

            # Progress report
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

    if processed_frames == 0:
        raise RuntimeError("No frames were processed.")

    # Calculate benchmark metrics
    inference_seconds = sum(inference_times) / 1000

    inference_fps = (
        processed_frames / inference_seconds
        if inference_seconds > 0
        else 0
    )

    pipeline_fps = (
        processed_frames / total_time
        if total_time > 0
        else 0
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

    # Save one benchmark row
    benchmark_row = {
        "timestamp": timestamp,
        "model": args.model.name,
        "model_format": model_format,
        "video": args.video.name,
        "device": args.device,
        "image_size": args.imgsz,
        "confidence": args.conf,
        "max_frames": args.max_frames,
        "frames": processed_frames,
        "inference_fps": round(inference_fps, 2),
        "pipeline_fps": round(pipeline_fps, 2),
        "average_latency_ms": round(average_latency, 2),
        "median_latency_ms": round(median_latency, 2),
        "p95_latency_ms": round(p95_latency, 2),
        "total_time_seconds": round(total_time, 2),
        "process_ram_mb": round(ram_mb, 2),
    }

    save_benchmark(args.csv, benchmark_row)

    print(f"\nAnnotated video: {args.output}")
    print(f"Benchmark CSV: {args.csv}")
    print("\nBenchmark completed successfully.")


if __name__ == "__main__":
    main()
